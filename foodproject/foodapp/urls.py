from django.urls import path
from . import views


urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        '',
        views.index,
        name='home'
    ),


    # =========================
    # AUTHENTICATION
    # =========================

    path(
        'login/',
        views.login_page,
        name='login'
    ),

    path(
        'signup/',
        views.signup_page,
        name='signup'
    ),

    path(
        'logout/',
        views.logout_page,
        name='logout'
    ),


    # =========================
    # FOOD
    # =========================

    path(
        'food/',
        views.food_page,
        name='food'
    ),

    path(
        'food/<int:food_id>/',
        views.food_detail,
        name='food_detail'
    ),


    # =========================
    # SEARCH
    # =========================

    path(
        'search/',
        views.search_page,
        name='search'
    ),


    # =========================
    # RESTAURANTS
    # =========================

    path(
        'restaurants/',
        views.restaurants_page,
        name='restaurants'
    ),

    # Old route kept
    path(
        'restraunt/',
        views.restaurants_page,
        name='restraunt'
    ),

    # =========================
    # CART
    # =========================

    path(
        'cart/',
        views.cart_page,
        name='cart'
    ),

    path(
        'cart/add/<int:food_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/update/<int:cart_id>/',
        views.update_cart,
        name='update_cart'
    ),

    path(
        'cart/remove/<int:cart_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),


    # =========================
    # WISHLIST
    # =========================

    path(
        'wishlist/',
        views.wishlist_page,
        name='wishlist'
    ),

    path(
        'wishlist/toggle/<int:food_id>/',
        views.toggle_wishlist,
        name='toggle_wishlist'
    ),


    # =========================
    # CHECKOUT
    # =========================

    path(
        'checkout/',
        views.checkout_page,
        name='checkout'
    ),

    path(
        'place-order/',
        views.place_order,
        name='place_order'
    ),


    # =========================
    # PAYMENT
    # =========================

    path(
        'payment/<int:order_id>/',
        views.payment_page,
        name='payment'
    ),

    path(
        'payment-success/<int:order_id>/',
        views.payment_success,
        name='payment_success'
    ),


    # =========================
    # ORDERS
    # =========================

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'order/<int:order_id>/',
        views.order_detail,
        name='order_detail'
    ),


    # =========================
    # PROFILE
    # =========================

    path(
        'profile/',
        views.profile_page,
        name='profile'
    ),

    path(
        'address/add/',
        views.add_address,
        name='add_address'
    ),


    # =========================
    # REVIEWS
    # =========================

    path(
        'reviews/',
        views.reviews_page,
        name='reviews'
    ),

    path(
        'review/<int:food_id>/',
        views.add_review,
        name='add_review'
    ),


    # =========================
    # CONTACT
    # =========================

    path(
        'contact/',
        views.contact_page,
        name='contact'
    ),


    # =========================
    # COMMENTS
    # =========================

    path(
        'comments/',
        views.comment_page,
        name='comments'
    ),


    # =========================
    # ADMIN DASHBOARD
    # =========================

    path(
        'dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'dashboard/orders/',
        views.admin_orders,
        name='admin_orders'
    ),

    path(
        'dashboard/customers/',
        views.admin_customers,
        name='admin_customers'
    ),
]