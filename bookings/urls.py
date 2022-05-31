#
from django.urls import path

from . import views

app_name = "bookings_app"

urlpatterns = [
    path('reservas/', views.BookingsView.as_view(), name='bookings'),
]