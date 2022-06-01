from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

# Create your views here.
from .models import Booking

class BookingsView(LoginRequiredMixin, TemplateView):
    template_name = 'bookings/bookings.html'
    
class MyBookingsView(LoginRequiredMixin, ListView):
    template_name = 'bookings/my_bookings.html'
    context_object_name = 'bookings'

    def get_queryset(self):
        today = timezone.now()
        qs = Booking.objects.filter(users=self.request.user, start__gte=today)
        return qs
