from rest_framework.routers import DefaultRouter

from django.urls import path, include

from .views import UserViewSet

router = DefaultRouter()
router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    # path('request-password-reset-email/', RequestPasswordResetEmail.as_view(), name='request-password-reset-email'),
    # path('password-reset/<str:uidb64>/<str:token>/', PasswordTokenCheck.as_view(), name='password-reset-check'),
]
