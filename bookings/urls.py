#
from django.urls import path

from . import views

app_name = "bookings_app"

urlpatterns = [
    path('bookings/', views.BookingsView.as_view(), name='bookings'),
    path('my-bookings/', views.MyBookingsView.as_view(), name='my-bookings'),
]