from django.urls import path
from ecommerceapp import views

urlpatterns = [
    path('',views.index,name="index"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('profile',views.profile,name="profile"),
    path('checkout/',views.checkout,name="checkout"),
    path('payment/',views.pay,name="payment"),
    path('payment-stage/',views.paytm,name="payment-stage"),
    path('payment-status/',views.pay,name="payment-status"),
    path('termsofservice/',views.terms,name="termsofservice"),
    path('privacypolicy/',views.privacy,name="privacypolicy"),
    path('service/<int:service_id>/', views.service_detail, name='service_detail'),
    path('service/book/', views.book_appointment, name='book_appointment'),
    path('services/', views.services_list, name='services_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('api/product/<int:product_id>/', views.product_api, name='product_api'),# Updated to use product_id
    path('mens/', views.mens_collection, name='mens_collection'),
    path('womens/', views.womens_collection, name='womens_collection'),
    path('api/cart/add/', views.cart_add, name='cart_add'),
    path('api/cart/remove/', views.cart_remove, name='cart_remove'),
    path('api/cart/update/', views.cart_update, name='cart_update'),
    path('api/cart/clear/', views.cart_clear, name='cart_clear'),
    path('api/cart/info/', views.cart_info, name='cart_info'),
]