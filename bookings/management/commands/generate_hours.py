from django.core.management.base import BaseCommand
from bookings.models import Hours
from datetime import time

class Command(BaseCommand):
    help = 'Generate table of hours'


    def handle(self, *args, **options):
        days = {
            '1':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            '2':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            '3':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            '4':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            '5':[time(9), time(10), time(11), time(12), time(13)],
        }
        
        for day, hours in days.items():
            for hour in hours:
                Hours.objects.create(day_of_week=day, hour=hour)