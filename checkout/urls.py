from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('create_payment_intent/', views.create_payment_intent, name='create_payment_intent'),
    path('checkout_success/<order_number>/', views.checkout_success, name='checkout_success'),
]
