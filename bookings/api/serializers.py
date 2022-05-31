from rest_framework import serializers
from rest_framework import status

from bookings.models import Booking
from users.models import User

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
        )
    

class BookingSerializer(serializers.ModelSerializer):
    
    users = UsersSerializer(many=True)
    
    class Meta:
        model = Booking
        exclude = ['created_at', 'updated_at']
        

    
    