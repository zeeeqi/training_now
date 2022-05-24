from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
#
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    )

    email = models.EmailField('Correo electrónico', unique='True')
    first_name = models.CharField('Nombre', max_length=30, blank=True)
    last_name = models.CharField('Apellidos', max_length=50, blank=True)
    gender = models.CharField('Género', max_length=1, choices=GENDER_CHOICES, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = []

    objects = UserManager()
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def get_name(self):
        return self.first_name
    
    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'