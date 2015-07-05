from datetime import datetime, timedelta
import pytz

from django.shortcuts import get_object_or_404
from django.contrib.auth import login, logout
from rest_framework import mixins, generics, renderers, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token

from .serializers import PoolUserSerializer
from .models import PoolUser

class CreateUser(generics.GenericAPIView):

    """ Creates Pool user for API call from """

    serializer_class = PoolUserSerializer
    queryset = PoolUser.objects.all()
    renderer_classes = (renderers.JSONRenderer,)

    def post(self, request, *args, **kwargs):
        data = request.DATA
        try:
            username = data['username']
            get_object_or_404(PoolUser,
                              username=username)
            return Response({
                'status': -1,
                'errors': 'User with username %s already exists' % username})
        except:
            pass
        mandatory_fields = [
            'password', 'username', 'first_name', 'email'
        ]
        errors = {}
        for field in mandatory_fields:
            if field not in data:
                errors[field] = ['This field is required']
        if errors:
            return Response({'status': -1, 'errors': errors})
        serializer = PoolUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': 1})
        return Response({'status': -1, 'errors': serializer.errors})


class UserLogin(generics.GenericAPIView):

    """ Api for Login """

    serializer_class = AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            previous_login = serializer.validated_data['user'].last_login
            login(request, serializer.validated_data['user'])
            token, created = Token.objects.get_or_create(
                user=serializer.validated_data['user'])
            if not created:
                utc_now = datetime.utcnow().replace(tzinfo=pytz.utc)
                if token.created < utc_now - timedelta(hours=24):
                    token.delete()
                    token, created = Token.objects.get_or_create(
                        user=serializer.validated_data['user'])
            user = request.user
            user.previous_login = previous_login
            user.save()
            return Response({'status': 1,
                             'token': token.key,
                             'first_name': request.user.first_name,
                             'last_name': request.user.last_name,
                             'username': request.user.username})
        return Response({'status': -1, "error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
