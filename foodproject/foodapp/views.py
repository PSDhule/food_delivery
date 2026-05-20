from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Food, Order, Contact, comment
from django.http import JsonResponse


# Home Page
def index(request):
    return render(request, 'index.html')


# Food Page
def food_page(request):

    foods = Food.objects.all()

    return render(request, 'food.html', {'foods': foods})


# Search Page
def search_page(request):

    query = request.GET.get('search')

    if query:

        foods = Food.objects.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )

    else:

        foods = Food.objects.all()

    context = {
        'foods': foods,
        'query': query
    }

    return render(request, 'search.html', context)


# Login Page
def login_page(request):

    message = ""

    if request.method == "POST":

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/food/')

        else:

            message = "Invalid Username or Password"

    return render(request, 'login.html', {'message': message})


# Signup Page
def signup_page(request):

    message = ""

    if request.method == "POST":

        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password != confirm_password:

            message = "Passwords do not match"

        elif User.objects.filter(username=username).exists():

            message = "Username already exists"

        else:

            User.objects.create_user(
                username=username,
                email=email,
                password=password
            )

            return redirect('/login/')

    return render(request, 'signup.html', {'message': message})


# Cart Page
def cart_page(request):

    food_name = request.GET.get('food_name')
    price = int(request.GET.get('price'))
    quantity = int(request.GET.get('quantity'))

    total = price * quantity

    food = Food.objects.get(name=food_name)

    context = {
        'food_name': food_name,
        'price': price,
        'quantity': quantity,
        'total': total,
        'image': food.image
    }

    return render(request, 'cart.html', context)


# Payment Page
def payment_page(request):

    food_name = request.GET.get('food_name')
    price = int(request.GET.get('price'))
    quantity = int(request.GET.get('quantity'))

    total = price * quantity

    food = Food.objects.get(name=food_name)

    context = {
        'food_name': food_name,
        'price': price,
        'quantity': quantity,
        'total': total,
        'image': food.image
    }

    return render(request, 'payment.html', context)


# Place Order
def place_order(request):

    food_name = request.GET.get('food_name')
    price = int(request.GET.get('price'))
    quantity = int(request.GET.get('quantity'))

    total = price * quantity

    food = Food.objects.get(name=food_name)

    Order.objects.create(
        food_name=food_name,
        price=price,
        quantity=quantity,
        total=total,
        image=food.image
    )

    return redirect('/order/')


# Order Page
def order_page(request):

    return render(request, 'order.html')


# My Orders Page
def myorder_page(request):

    orders = Order.objects.all()

    return render(request, 'myorder.html', {'orders': orders})

# Save Rating
def save_rating(request):

    order_id = request.GET.get('order_id')

    rating = request.GET.get('rating')

    order = Order.objects.get(id=order_id)

    order.rating = rating

    order.save()

    return JsonResponse({
        'message': 'Rating Saved'
    })

# Contact Page
def contact_page(request):

    message = ""

    if request.method == "POST":

        name = request.POST['name']

        email = request.POST['email']

        user_message = request.POST['message']

        Contact.objects.create(
            name=name,
            email=email,
            message=user_message
        )

        message = "Message Sent Successfully"

    return render(
        request,
        'contact.html',
        {'message': message}
    )

def comment_page(request):

    if request.method == "POST":

        name = request.POST.get('name')
        user_comment = request.POST.get('comment')

        comment.objects.create(
            name=name,
            comment=user_comment
        )

    comments = comment.objects.all().order_by('-id')

    return render(request, 'comments.html', {'comments':comments})

def restraunt_page(request):

    return render(request, 'restraunt.html')
    