from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class UserViewSet(GenericViewSet):
    
    @action(methods=['GET'], detail=False, url_path='current-user')
    def current_user(self, request):
        user = request.user
        if user.is_authenticated:
            return Response(data={'id': user.id, 'name': user.first_name})
        return Response(data={'id': None, 'name': None})