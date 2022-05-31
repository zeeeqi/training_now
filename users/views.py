from django.core.mail import send_mail
from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect


from django.views.generic import (
    View,
    TemplateView
)

from django.views.generic.edit import (
    FormView
)

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UpdatePasswordForm,
    ContactForm
)
#
from .models import User



class UserRegisterView(FormView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = '/'

    def form_valid(self, form):
        user = User(
            email=form.cleaned_data['email'],
            first_name=form.cleaned_data['first_name'],
            last_name=form.cleaned_data['last_name'],
            gender=form.cleaned_data['gender'],
        )
        user.set_password(form.cleaned_data['password1'])
        user.save()

        return HttpResponseRedirect(
            reverse('users_app:user-login')
        )


class LoginUser(FormView):
    template_name = 'users/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('users_app:user-login')
    
    def get_success_url(self):
        if self.request.GET.get('next'):
            return self.request.GET.get('next')
        return super().get_success_url()

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super(LoginUser, self).get(request, *args, **kwargs)
    
    def form_valid(self, form):
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )
        login(self.request, user)
        remember_me = form.cleaned_data['remember_me']
        if not remember_me:
            self.request.session.set_expiry(0)
        
        return super(LoginUser, self).form_valid(form)


class LogoutView(View):
    def get(self, request, *args, **kargs):
        logout(request)
        return HttpResponseRedirect(reverse('users_app:user-login'))


class UpdatePasswordView(LoginRequiredMixin, FormView):
    template_name = 'users/update.html'
    form_class = UpdatePasswordForm
    success_url = reverse_lazy('users_app:user-login')

    def form_valid(self, form):
        user = authenticate(
            username=self.request.user.email,
            password=form.cleaned_data['password1']
        )

        if user:
            new_password = form.cleaned_data['password2']
            user.set_password(new_password)
            user.save()

        logout(self.request)
        return super(UpdatePasswordView, self).form_valid(form)

class IndexView(TemplateView):
    template_name = 'home/index.html'
    
class ContactFormView(FormView):
    template_name = 'home/contact.html'
    form_class = ContactForm
    success_url = '/'
    
    def form_valid(self, form):
        data = form.data
        subject = data['subject']
        message = data['message']
        email = data['email']
        name = data['name']
        sender = settings.EMAIL_HOST_USER
        send_mail(
            f'{name} se ha puesto en contacto a través del formulario web.',
            f'{name} con el email {email} se ha puesto en contacto con nosotros.\nASUNTO\n{subject}\n-------------------------------------------------\nMENSAJE\n{message}',
            sender,
            ['ezequielarenilla@gmail.com']
        )
        return super(ContactFormView, self).form_valid(form)