from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import GenericAPIView
from rest_framework import status

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.html import strip_tags


from .serializers import RequestPasswordResetEmailSerializer


User = get_user_model()

class UserViewSet(GenericViewSet):
    
    @action(methods=['GET'], detail=False, url_path='current-user')
    def current_user(self, request):
        user = request.user
        if user.is_authenticated:
            return Response(data={'id': user.id, 'name': user.first_name})
        return Response(data={'id': None, 'name': None})
    

# class RequestPasswordResetEmail(GenericAPIView):
    
#     serializer_class = RequestPasswordResetEmailSerializer
    
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         email = request.data.get('email', '')
#         user = User.objects.filter(email=email).first()
#         if user:
#             uidb64 = urlsafe_base64_encode(force_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             current_site = get_current_site(request)
#             domain = current_site.domain
#             protocol = 'https://' if request.is_secure() else 'http://'
#             relative_link = reverse('password-reset-check', kwargs={'uidb64': uidb64, 'token': token})
#             reset_url = f'{protocol}{domain}{relative_link}'
#             html_message = render_to_string(
#                 'emails/reset_password.html',
#                 {
#                     'name': user.first_name,
#                     'reset_url': reset_url,
#                     'domain': domain,
#                     'protocol': protocol,
#                 }
#             )
#             plain_message = strip_tags(html_message)
#             send_mail('Restablecimiento de contraseña',plain_message, settings.DEFAULT_FROM_EMAIL, [user.email], html_message=html_message)        
        
#         return Response(
#             {'success': 'Si el correo es correcto, se le enviará un enlace para restablecer su contraseña'},
#             status=status.HTTP_200_OK
#         )
        
# class PasswordTokenCheck(GenericAPIView):
    
#     def get(self, request, uidb64, token):
        
#         id = smart_str(urlsafe_base64_decode(uidb64))
#         user = User.objects.filter(id=id).first()
        
#         if user:
#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response(
#                     {'error': 'El token es inválido'},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
            
#             return Response(
#                 {
#                     'success': 'El token es válido',
#                     'uidb64':uidb64,
#                     'token':token
#                 }, 
#                 status=status.HTTP_200_OK, 
#             )