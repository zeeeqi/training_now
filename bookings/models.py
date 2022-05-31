from django.db import models

from users.models import User
from .managers import BookingManager
# Create your models here.

class Booking(models.Model):
    
    users = models.ManyToManyField(User, related_name='bookings', verbose_name='Usuarios', blank=True)
    
    start = models.DateTimeField('Inicio', auto_now=False, auto_now_add=False, unique=True)
    max_people = models.IntegerField('Maximo de personas', default=4)
    allow_inscriptions = models.BooleanField('Permitir inscripciones', default=True)
    
    created_at = models.DateTimeField('Creado', auto_now_add=True)
    updated_at = models.DateTimeField('Actualizado', auto_now=True)
    
    objects = models.Manager()
    
    planner = BookingManager()
    
    class Meta:
        verbose_name = 'Clase'
        verbose_name_plural = 'Clases'
        ordering = ['start']
    
    def __str__(self):
        return f'{self.start.strftime("%A - %d/%m/%Y %H:%M")}'


DAYS_OF_WEEK = (
    ('1', 'Lunes'),
    ('2', 'Martes'),
    ('3', 'Miercoles'),
    ('4', 'Jueves'),
    ('5', 'Viernes'),
    ('6', 'Sabado'),
    ('7', 'Domingo'),
)

ISO_WEEK_DAYS = ('Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes', 'Sabado', 'Domingo')
class Hours(models.Model):
    
    day_of_week = models.CharField('Dia de la semana', max_length=10, choices=DAYS_OF_WEEK)
    hour = models.TimeField('Hora')
    
    
    class Meta:
        verbose_name = 'Hora'
        verbose_name_plural = 'Horas'
        unique_together = ('day_of_week', 'hour')
        
    
    
    def __str__(self):
        return f'{ISO_WEEK_DAYS[int(self.day_of_week)-1]} - {self.hour.strftime("%H:%M")}'
    