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
    path('privacypolicy/',views.privacy,name="privacypolicy")
]