from django.urls import path, include
from bookings.api.urls import urlpatterns as booking_urls

urlpatterns = [
    path('', include(booking_urls)),
]