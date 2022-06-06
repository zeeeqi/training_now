from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class BookingsView(LoginRequiredMixin, TemplateView):
    template_name = 'bookings/bookings.html'
    
class MyBookingsView(LoginRequiredMixin, TemplateView):
    template_name = 'bookings/my_bookings.html'
    