import random

from django.db import models
from django.contrib.auth.models import AbstractUser
#
class User(AbstractUser):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    email = models.EmailField('Correo electrónico', unique='True')
    first_name = models.CharField('Nombre', max_length=30, blank=True)
    last_name = models.CharField('Apellidos', max_length=50, blank=True)
    gender = models.CharField('Género', max_length=1, choices=GENDER_CHOICES, blank=True)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.full_name} - {self.email}'
    
    def save(self, **kwargs):
        self.username = f'{self.email.rsplit("@", 1)[0]}_{random.randint(1, 100)}'
        super().save(**kwargs)

    def get_name(self):
        return self.first_name
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'