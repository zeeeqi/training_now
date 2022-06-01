from django.urls import path, include
from bookings.api.urls import urlpatterns as booking_urls
from users.api.urls import urlpatterns as users_urls

urlpatterns = [
    path('', include(booking_urls)),
    path('', include(users_urls)),
]