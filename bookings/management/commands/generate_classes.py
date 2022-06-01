from datetime import datetime, timezone, timedelta
from django.core.management.base import BaseCommand
from bookings.models import Booking


class Command(BaseCommand):
    help = 'Generate next month of available hours'


    def handle(self, *args, **options):
        start_date = Booking.objects.all().order_by('-start').first()
        if not start_date:
            start_date = datetime.now(timezone.utc)
        else:
            start_date = start_date.start
            
        end_date = datetime.now(timezone.utc) + timedelta(days=30)

        for day in range((end_date - start_date).days):
            Booking.planner.create_day(start_date + timedelta(days=day + 1))