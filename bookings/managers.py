from django.db import models
from datetime import datetime, timedelta, time, timezone


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

        for day in range(0, (end_date - start_date).days):
            self.create_day(start_date + timedelta(days=day + 1))
            
    def create_day(self, date):
        day_str = date.strftime("%A").lower()
        allowed_hours = self.get_hours(day_str)
        
        for hour in allowed_hours:
            self.create_booking(start=datetime.combine(date, hour))
    
    def add_user(self, booking, user):
        if booking.users.count() < booking.max_people:
            booking.users.add(user)
            booking.save()
            
        
    @staticmethod
    def get_hours(day_str):
        days = {
            'monday':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            'tuesday':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            'wednesday':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            'thursday':[time(9), time(10), time(11), time(12), time(13), time(15), time(16), time(17), time(18), time(19), time(20), time(21)],
            'friday':[time(9), time(10), time(11), time(12), time(13)],
        }
        return days.get(day_str, [])