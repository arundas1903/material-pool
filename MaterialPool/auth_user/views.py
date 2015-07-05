from datetime import datetime, timedelta
import pytz

from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from django.http import Http404
from rest_framework import generics, renderers, permissions, status
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

    """ Api for Login and Logout"""

    serializer_class = AuthTokenSerializer
    renderer_classes = (renderers.JSONRenderer, )

    def post(self, request, *args, **kwargs):
        data = request.DATA
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
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
            user.save()
            return Response({'status': 1,
                             'token': token.key,
                             'first_name': request.user.first_name,
                             'last_name': request.user.last_name,
                             'username': request.user.username})
        try:
            user = get_object_or_404(PoolUser, username=data['username'])
            password = user.check_password(data['password'])
            if not password:
                return Response({'status': -1, 'errors': 'Invalid Password'})
        except:
            return Response({'status': -1, 'errors': 'Invalid Username'})
        return Response({'status': -1, "error": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if token:
            try:
                token_obj = get_object_or_404(Token, key=token.split()[1])
                token_obj.delete()
            except Http404:
                pass
        return Response({'status': 1, 'token': None})


class ChangePassword(generics.GenericAPIView):

    """Api to change password"""

    renderer_classes = (renderers.JSONRenderer,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")
        if password and confirm_password:
            pass
        else:
            return Response(
                {
                    'status': -1,
                    'errors': 'Please enter password to be changed'
                }
            )
        if password == confirm_password:
            user = request.user
            if user.check_password(password):
                return Response(
                    {
                        "status": -1,
                        "errors": "Please enter a new password to change"}
                )
            user.set_password(password)
            user.save()
            return Response({"status": 1})
        else:
            return Response(
                {"status": -1, "errors": "Passwords did not match"}
            )
