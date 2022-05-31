from rest_framework.routers import DefaultRouter
from .views import BookingViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('bookings', BookingViewSet, basename='bookings')

urlpatterns = [
    path('', include(router.urls)),
]
