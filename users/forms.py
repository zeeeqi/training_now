from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
#
from .models import User

import re

class UserRegisterForm(forms.ModelForm):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control'
            }
        ),
        validators=[
            validate_password
        ]
    )
    password2 = forms.CharField(
        label='Repetir Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Repetir Contraseña',
                'class': 'form-control'
            }
        ),
        validators=[
            validate_password
        ]
    )
    
    field_order = ['email', 'password1', 'password2', 'first_name', 'last_name', 'gender']

    class Meta:
        model = User
        fields = (
            'email',
            'first_name',
            'last_name',
            'gender',
        )
        widgets = {
            'email': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Correo electrónico'
                }
            ),
            'first_name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Nombre'
                }
            ),
            'last_name': forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder': 'Apellidos'
                }
            ),
            'gender': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),
        }
        
    def clean(self):
        user = User.objects.filter(email=self.cleaned_data['email']).count()
        if user:
            raise forms.ValidationError('El correo electrónico ya está registrado')
    
    def clean_password2(self):
        if self.cleaned_data['password1'] != self.cleaned_data['password2']:
            self.add_error('password2', 'Las contraseñas no son iguales')
         

class LoginForm(forms.Form):
    email = forms.CharField(
        label='Email',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
                'class': 'form-control form-control-lg',
                'id': 'form2Example17'
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña',
                'class': 'form-control form-control-lg',
                'id': 'form2Example27'
            }
        )
    )
    
    remember_me = forms.BooleanField(
        label='Recordarme',
        required=False,
        initial=True,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-check-input',
            }
        )
        );

    def clean(self):
        self.cleaned_data = super(LoginForm, self).clean()
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']

        if not authenticate(email=email, password=password):
            raise forms.ValidationError('Email o contraseña incorrectos')
        
        return self.cleaned_data


class UpdatePasswordForm(forms.Form):

    password1 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Actual'
            }
        )
    )
    password2 = forms.CharField(
        label='Contraseña',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Contraseña Nueva'
            }
        )
    )


class VerificationForm(forms.Form):
    codregistro = forms.CharField(required=True)


    def __init__(self, pk, *args, **kwargs):
        self.id_user = pk
        super(VerificationForm, self).__init__(*args, **kwargs)

    def clean_codregistro(self):
        codigo = self.cleaned_data['codregistro']

        if len(codigo) == 6:
            # verificamos si el codigo y el id de usuario son validos:
            activo = User.objects.cod_validation(
                self.id_user,
                codigo
            )
            if not activo:
                raise forms.ValidationError('el codigo es incorrecto')
        else:
            raise forms.ValidationError('el codigo es incorrecto')
        

class ContactForm(forms.Form):
    name = forms.CharField(
        label='Nombre',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nombre',
                'class': 'form-control'
            }
        )
    )
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Correo electrónico',
                'class': 'form-control',
            }
        )
    )
    subject = forms.CharField(
        label='Asunto',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Asunto',
                'class': 'form-control'
            }
        )
    )
    message = forms.CharField(
        label='Mensaje',
        required=True,
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Mensaje',
                'class': 'form-control',
                'rows': '50'
            }
        )
    )
    
    captcha = ReCaptchaField(
        widget=ReCaptchaV2Checkbox,
        label="",
    )
    
    def clean_name(self):
        if len(self.cleaned_data['name']) < 5:
            self.add_error('name', 'El nombre debe tener al menos 5 caracteres')
    
    def clean_email(self):
        valid_email = re.match(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$', self.cleaned_data['email'])
        if not valid_email:
            self.add_error('email', 'El email no es valido')
    
    def clean_subject(self):
        if len(self.cleaned_data['subject']) < 5:
            self.add_error('subject', 'El asunto debe tener al menos 5 caracteres')
        
    def clean_message(self):
        if len(self.cleaned_data['message']) < 10:
            self.add_error('message', 'El mensaje debe tener al menos 10 caracteres')
        elif len(self.cleaned_data['message']) > 500:
            self.add_error('message', 'El mensaje no puede tener mas de 500 caracteres')
    
    def clean(self):
        self.cleaned_data = super(ContactForm, self).clean()
        
        return self.cleaned_data