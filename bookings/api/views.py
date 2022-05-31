from datetime import datetime

from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers

from bookings.models import Booking
from .serializers import BookingSerializer


class BookingViewSet(GenericViewSet):
    
    
    def get_queryset(self):
        if self.action == 'get_bookings':
            start_date = self.request.query_params.get('start_date')
            end_date = datetime.strptime(self.request.query_params.get('end_date'), '%Y-%m-%d').replace(hour=23, minute=59, second=59)
            qs = Booking.objects.filter(start__gte=start_date, start__lte=end_date)
        
        return qs
    
    def get_serializer_class(self):
        if self.action == 'get_bookings':
            return BookingSerializer
        
        return serializers.Serializer
    
    
    @action(methods=['get'], detail=False, url_path='get-bookings')
    def get_bookings(self, request):
        
        qs = self.get_queryset()
        
        return Response(data=self.get_serializer_class()(qs, many=True).data)
        
    @action(methods=['POST','DELETE'], detail=True, url_path='create-booking')
    def create_booking(self, request, pk):
        booking = Booking.objects.filter(pk=pk).first()
        if booking:
            user = request.user
            if user.is_authenticated:
                print(request.method)
                if request.method == 'POST':
                    start = booking.start.replace(hour=0, minute=0, second=0)
                    end = start.replace(hour=23, minute=59, second=59)
                    
                    if Booking.objects.filter(start__range=(start, end), users=user).exists():
                        return Response(data={'message': 'Ya tienes una reserva para hoy'}, status=status.HTTP_400_BAD_REQUEST)
                    if booking.users.filter(id=user.id).exists():
                        return Response(data={'message': 'Ya estás en esta clase'}, status=status.HTTP_400_BAD_REQUEST)
                    if booking.max_people == booking.users.count():
                        return Response(data={'message': 'La clase está llena'}, status=status.HTTP_400_BAD_REQUEST)
                    if booking.allow_inscriptions:
                        booking.users.add(user)
                        return Response(data={'message': 'Clase reservada con éxito'}, status=status.HTTP_201_CREATED)
                    else:
                        return Response(data={'message': 'La clase no permite inscripciones'}, status=status.HTTP_400_BAD_REQUEST)
                elif request.method == 'DELETE':
                    if booking.users.filter(id=user.id).exists():
                        booking.users.remove(user)
                        return Response(data={'message': 'Clase cancelada con éxito'}, status=status.HTTP_200_OK)
                    else:
                        return Response(data={'message': 'No estás inscrito en esta clase'}, status=status.HTTP_400_BAD_REQUEST)
                        
               
        return Response(status=status.HTTP_200_OK)
        
        
    @action(methods=['GET'], detail=False, url_path='current-user')
    def current_user(self, request):
        user = request.user
        if user.is_authenticated:
            return Response(data={'id': user.id, 'name': user.first_name})
        return Response(data={'id': None, 'name': None})