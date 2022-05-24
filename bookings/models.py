from django.db import models

from users.models import User
from .managers import BookingManager
# Create your models here.

class Booking(models.Model):
    
    users = models.ManyToManyField(User, related_name='bookings', verbose_name='Usuarios')
    
    start = models.DateTimeField('Inicio', auto_now=False, auto_now_add=False, unique=True)
    max_people = models.IntegerField('Maximo de personas', default=4)
    allow_inscriptions = models.BooleanField('Permitir inscripciones', default=True)
    
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    
    objects = BookingManager()
    
    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
        ordering = ['start']
    
    def __str__(self):
        return f'{self.start.strftime("%A - %d/%m/%Y %H:%M")}'
