from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q, Sum
from django.contrib import messages

from .models import (
    Food,
    Restaurant,
    Cart,
    Wishlist,
    Order,
    OrderItem,
    Review,
    Address,
    Contact,
    comment
)


# =========================
# HOME
# =========================

def index(request):
    foods = Food.objects.filter(
        is_available=True
    ).order_by('-id')[:8]

    restaurants = Restaurant.objects.filter(
        is_active=True
    ).order_by('-id')[:6]

    return render(
        request,
        'index.html',
        {
            'foods': foods,
            'restaurants': restaurants
        }
    )


# =========================
# AUTHENTICATION
# =========================

def login_page(request):

    if request.user.is_authenticated:
        return redirect('food')

    message = ""

    next_url = request.GET.get('next')

    if request.method == "POST":

        username = request.POST.get(
            'username',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            if next_url:
                return redirect(next_url)

            return redirect('food')

        message = "Invalid username or password."

    return render(
        request,
        'login.html',
        {
            'message': message
        }
    )


def signup_page(request):

    if request.user.is_authenticated:
        return redirect('food')

    message = ""

    if request.method == "POST":

        username = request.POST.get(
            'username',
            ''
        ).strip()

        email = request.POST.get(
            'email',
            ''
        ).strip()

        password = request.POST.get(
            'password',
            ''
        )

        confirm_password = request.POST.get(
            'confirm_password',
            ''
        )

        if not username or not email or not password:

            message = "Please fill all fields."

        elif password != confirm_password:

            message = "Passwords do not match."

        elif User.objects.filter(
            username=username
        ).exists():

            message = "Username already exists."

        elif User.objects.filter(
            email=email
        ).exists():

            message = "Email already exists."

        else:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            messages.success(
                request,
                "Account created successfully. Please login."
            )

            return redirect('login')

    return render(
        request,
        'signup.html',
        {'message': message}
    )


@login_required
def logout_page(request):

    logout(request)

    return redirect('home')


# =========================
# FOOD
# =========================

@login_required(login_url='/login/')
def food_page(request):

    foods = Food.objects.filter(
        is_available=True
    ).select_related('restaurant')

    category = request.GET.get(
        'category',
        ''
    ).strip()

    min_price = request.GET.get(
        'min_price',
        ''
    ).strip()

    max_price = request.GET.get(
        'max_price',
        ''
    ).strip()

    if category:
        foods = foods.filter(
            category__icontains=category
        )

    if min_price.isdigit():
        foods = foods.filter(
            price__gte=int(min_price)
        )

    if max_price.isdigit():
        foods = foods.filter(
            price__lte=int(max_price)
        )

    categories = Food.objects.values_list(
        'category',
        flat=True
    ).distinct()

    return render(
        request,
        'food.html',
        {
            'foods': foods,
            'categories': categories,
            'selected_category': category,
            'min_price': min_price,
            'max_price': max_price
        }
    )

@login_required(login_url='login')
def food_detail(request, food_id):

    food = get_object_or_404(
        Food,
        id=food_id
    )

    reviews = Review.objects.filter(
        food=food
    ).select_related('user').order_by('-id')

    related_foods = Food.objects.filter(
        category=food.category,
        is_available=True
    ).exclude(
        id=food.id
    )[:4]

    is_wishlisted = False

    if request.user.is_authenticated:

        is_wishlisted = Wishlist.objects.filter(
            user=request.user,
            food=food
        ).exists()

    return render(
        request,
        'food_detail.html',
        {
            'food': food,
            'reviews': reviews,
            'related_foods': related_foods,
            'is_wishlisted': is_wishlisted
        }
    )


# =========================
# SEARCH
# =========================

def search_page(request):

    query = request.GET.get(
        'search',
        ''
    ).strip()

    restaurant_id = request.GET.get(
        'restaurant',
        ''
    ).strip()

    foods = Food.objects.filter(
        is_available=True
    ).select_related('restaurant')

    restaurant = None

    # =========================
    # RESTAURANT FILTER
    # =========================

    if restaurant_id.isdigit():

        restaurant = get_object_or_404(
            Restaurant,
            id=int(restaurant_id),
            is_active=True
        )

        foods = foods.filter(
            restaurant_id=restaurant.id
        )

    # =========================
    # NORMAL SEARCH
    # =========================

    if query:

        foods = foods.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query) |
            Q(description__icontains=query)
        )

    return render(
        request,
        'search.html',
        {
            'foods': foods,
            'query': query,
            'restaurant': restaurant
        }
    )

# =========================
# RESTAURANTS
# =========================

def restaurants_page(request):

    restaurants = Restaurant.objects.filter(
        is_active=True
    ).order_by('-rating', 'name')

    return render(
        request,
        'restaurants.html',
        {
            'restaurants': restaurants
        }
    )


# =========================
# CART
# =========================

@login_required
def add_to_cart(request, food_id):

    food = get_object_or_404(
        Food,
        id=food_id,
        is_available=True
    )

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        food=food
    )

    if not created:
        cart_item.quantity += 1

    cart_item.save()

    messages.success(
        request,
        f"{food.name} added to cart."
    )

    return redirect('cart')


@login_required
def cart_page(request):

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related('food')

    subtotal = sum(
        item.total_price()
        for item in cart_items
    )

    delivery_charge = 40 if subtotal > 0 else 0

    grand_total = subtotal + delivery_charge

    return render(
        request,
        'cart.html',
        {
            'cart_items': cart_items,
            'subtotal': subtotal,
            'delivery_charge': delivery_charge,
            'grand_total': grand_total
        }
    )


@login_required
def update_cart(request, cart_id):

    item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    if request.method == "POST":

        quantity = request.POST.get(
            'quantity',
            '1'
        )

        if quantity.isdigit():

            quantity = int(quantity)

            if quantity > 0:
                item.quantity = quantity
                item.save()

            else:
                item.delete()

    return redirect('cart')


@login_required
def remove_from_cart(request, cart_id):

    item = get_object_or_404(
        Cart,
        id=cart_id,
        user=request.user
    )

    item.delete()

    messages.success(
        request,
        "Item removed from cart."
    )

    return redirect('cart')


# =========================
# WISHLIST
# =========================

@login_required
def wishlist_page(request):

    wishlist_items = Wishlist.objects.filter(
        user=request.user
    ).select_related('food')

    return render(
        request,
        'wishlist.html',
        {
            'wishlist_items': wishlist_items
        }
    )


@login_required
def toggle_wishlist(request, food_id):

    food = get_object_or_404(
        Food,
        id=food_id
    )

    item = Wishlist.objects.filter(
        user=request.user,
        food=food
    ).first()

    if item:

        item.delete()

        messages.success(
            request,
            "Removed from wishlist."
        )

    else:

        Wishlist.objects.create(
            user=request.user,
            food=food
        )

        messages.success(
            request,
            "Added to wishlist."
        )

    return redirect(
        request.META.get(
            'HTTP_REFERER',
            'food'
        )
    )


# =========================
# CHECKOUT
# =========================

@login_required
def checkout_page(request):

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related('food')

    if not cart_items.exists():

        messages.warning(
            request,
            "Your cart is empty."
        )

        return redirect('food')

    addresses = Address.objects.filter(
        user=request.user
    )

    subtotal = sum(
        item.total_price()
        for item in cart_items
    )

    delivery_charge = 40

    grand_total = subtotal + delivery_charge

    return render(
        request,
        'checkout.html',
        {
            'cart_items': cart_items,
            'addresses': addresses,
            'subtotal': subtotal,
            'delivery_charge': delivery_charge,
            'grand_total': grand_total
        }
    )


@login_required
def place_order(request):

    if request.method != "POST":

        return redirect('checkout')

    cart_items = Cart.objects.filter(
        user=request.user
    ).select_related('food')

    if not cart_items.exists():

        return redirect('cart')

    address_id = request.POST.get(
        'address_id'
    )

    payment_method = request.POST.get(
        'payment_method',
        'COD'
    )

    # Special instruction from checkout
    special_instruction = request.POST.get(
        'special_instruction',
        ''
    ).strip()

    address = get_object_or_404(
        Address,
        id=address_id,
        user=request.user
    )

    subtotal = sum(
        item.total_price()
        for item in cart_items
    )

    delivery_charge = 40

    grand_total = subtotal + delivery_charge

    order_address = (
        f"{address.full_name}, "
        f"{address.phone}, "
        f"{address.address_line}, "
        f"{address.city}, "
        f"{address.state} - "
        f"{address.pincode}"
    )

    # Create Order
    order = Order.objects.create(

        user=request.user,

        total=grand_total,

        address=order_address,

        special_instruction=special_instruction,

        payment_method=payment_method,

        payment_status=(
            'Paid'
            if payment_method == 'Online'
            else 'Pending'
        ),

        status=(
            'Confirmed'
            if payment_method == 'COD'
            else 'Pending'
        )
    )

    # Create Order Items
    for item in cart_items:

        OrderItem.objects.create(

            order=order,

            food=item.food,

            quantity=item.quantity,

            price=item.food.price,

            total=item.total_price()
        )

    # Keep old fields populated
    first_item = cart_items.first()

    if first_item:

        order.food_name = first_item.food.name

        order.price = first_item.food.price

        order.quantity = first_item.quantity

        order.image = first_item.food.image

        order.save()

    # Clear cart
    cart_items.delete()

    # Online payment
    if payment_method == 'Online':

        return redirect(
            'payment',
            order_id=order.id
        )

    # COD
    return redirect(
        'order_detail',
        order_id=order.id
    )

# =========================
# PAYMENT DEMO
# =========================

@login_required
def payment_page(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'payment.html',
        {
            'order': order
        }
    )


@login_required
def payment_success(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    order.payment_status = 'Paid'
    order.status = 'Confirmed'
    order.save()

    return render(
        request,
        'payment_success.html',
        {
            'order': order
        }
    )


# =========================
# ORDERS
# =========================

@login_required
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).prefetch_related(
        'items'
    ).order_by('-created_at')

    return render(
        request,
        'my_orders.html',
        {
            'orders': orders
        }
    )


@login_required
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_detail.html',
        {
            'order': order
        }
    )


# =========================
# PROFILE
# =========================

@login_required
def profile_page(request):

    addresses = Address.objects.filter(
        user=request.user
    )

    return render(
        request,
        'profile.html',
        {
            'addresses': addresses
        }
    )


@login_required
def add_address(request):

    if request.method == "POST":

        Address.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address_line=request.POST.get('address_line'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            is_default=(
                request.POST.get('is_default') == 'on'
            )
        )

        messages.success(
            request,
            "Address added successfully."
        )

    return redirect('profile')


# =========================
# REVIEWS
# =========================

def reviews_page(request):

    reviews = Review.objects.select_related(
        'user',
        'food'
    ).order_by('-created_at')

    return render(
        request,
        'reviews.html',
        {
            'reviews': reviews
        }
    )


@login_required
def add_review(request, food_id):

    food = get_object_or_404(
        Food,
        id=food_id
    )

    if request.method == "POST":

        rating = request.POST.get(
            'rating',
            '5'
        )

        review_text = request.POST.get(
            'comment',
            ''
        ).strip()

        if rating.isdigit() and review_text:

            Review.objects.create(
                user=request.user,
                food=food,
                rating=int(rating),
                comment=review_text
            )

            messages.success(
                request,
                "Review added successfully."
            )

    return redirect(
        'food_detail',
        food_id=food.id
    )


# =========================
# CONTACT
# =========================

def contact_page(request):

    if request.method == "POST":

        Contact.objects.create(
            name=request.POST.get('name'),
            email=request.POST.get('email'),
            message=request.POST.get('message')
        )

        messages.success(
            request,
            "Your message has been sent."
        )

        return redirect('contact')

    return render(
        request,
        'contact.html'
    )


# =========================
# COMMENTS
# =========================

def comment_page(request):

    if request.method == "POST":

        comment.objects.create(
            name=request.POST.get('name'),
            comment=request.POST.get('comment')
        )

        return redirect('comments')

    comments = comment.objects.all().order_by('-id')

    return render(
        request,
        'reviews.html',
        {
            'comments': comments
        }
    )

# =========================
# ADMIN DASHBOARD
# =========================

def is_staff_user(user):

    return user.is_authenticated and user.is_staff


@user_passes_test(is_staff_user)
def admin_dashboard(request):

    total_foods = Food.objects.count()

    total_restaurants = Restaurant.objects.count()

    total_customers = User.objects.filter(
        is_staff=False
    ).count()

    total_orders = Order.objects.count()

    total_revenue = Order.objects.filter(
        status='Delivered'
    ).aggregate(
        total=Sum('total')
    )['total'] or 0

    return render(
        request,
        'admin_dashboard.html',
        {
            'total_foods': total_foods,
            'total_restaurants': total_restaurants,
            'total_customers': total_customers,
            'total_orders': total_orders,
            'total_revenue': total_revenue
        }
    )


@user_passes_test(is_staff_user)
def admin_orders(request):

    orders = Order.objects.select_related(
        'user'
    ).order_by('-created_at')

    return render(
        request,
        'admin_orders.html',
        {
            'orders': orders
        }
    )


@user_passes_test(is_staff_user)
def admin_customers(request):

    customers = User.objects.filter(
        is_staff=False
    ).order_by('-date_joined')

    return render(
        request,
        'admin_customers.html',
        {
            'customers': customers
        }
    )