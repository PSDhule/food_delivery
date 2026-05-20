from django.urls import path
from . import views

urlpatterns = [

    # Home Page
    path('',views.index, name='home'),

    # Food Page
    path('food/', views.food_page, name='food'),

    # Login Page
    path('login/', views.login_page, name='login'),

    # Signup Page
    path('signup/', views.signup_page, name='signup'),

     # Search Page
    path('search/', views.search_page, name='search'),

    # Cart Page
    path('cart/', views.cart_page, name='cart'),

    # Payment Page
    path('payment/', views.payment_page, name='payment'),

    path('placeorder/', views.place_order, name='placeorder'),
    
    # Order Page
    path('order/', views.order_page, name='order'),

    # MY ORDER PAGE
    path('myorder/', views.myorder_page, name='myorder'),

    path('save-rating/', views.save_rating, name='save_rating'),  

    path('contact/', views.contact_page, name='contact'),

    path('comments/', views.comment_page, name='comments'),  

    path('restraunt/', views.restraunt_page, name='restraunt'),
]