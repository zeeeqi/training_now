from django.db import models
from datetime import datetime, timedelta, time, timezone
from django.apps import apps

class BookingManager(models.Manager):
    
    def create_booking(self, start, max_people=4, allow_inscriptions=True):
        booking = self.create(
            start=start,
            max_people=max_people,
            allow_inscriptions=allow_inscriptions
        )
        return booking
    
    def create_bookings_next_month(self):
        start_date = self.order_by('-start').first()
        if not start_date:
            start_date = datetime.now(timezone.utc)
        else:
            start_date = start_date.start
            
        end_date = datetime.now(timezone.utc) + timedelta(days=30)

        for day in range((end_date - start_date).days):
            self.create_day(start_date + timedelta(days=day + 1))
            
    def create_day(self, date):
        Hours = apps.get_model('bookings','Hours') #Hours.objects.filter(day_of_week='0').order_by('hour')
        day_of_week = str(date.isoweekday())

        allowed_hours = Hours.objects.filter(day_of_week=day_of_week).order_by('hour')
        
        for hour in allowed_hours:
            self.create_booking(start=datetime.combine(date, hour.hour))
    
    def add_user(self, booking, user):
        if booking.users.count() < booking.max_people:
            booking.users.add(user)
            booking.save()
            
    
    def get_hours(day_str):
        days = {
            '0':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            '1':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            '2':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            '3':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            '4':[time(9), time(10), time(11), time(12), time(13)],
        }
        
                