from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:schedule_id>/', views.create_booking, name='create_booking'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
