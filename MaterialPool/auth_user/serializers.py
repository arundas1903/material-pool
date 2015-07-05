from rest_framework import serializers

from .models import PoolUser

class PoolUserSerializer(serializers.Serializer):

    """ Serializer for model PoolUser """

    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=30)
    first_name = serializers.CharField(max_length=30)
    last_name = serializers.CharField(max_length=30, required=False,
                                      allow_blank=True)
    email = serializers.EmailField(max_length=100, required=False)

    def create(self, validated_data):
        password = validated_data.get('password')
        email = validated_data.get('email')
        user = PoolUser.objects.create_user(
            validated_data.get('username'), email, password)
        user.first_name = validated_data.get('first_name')
        user.last_name = validated_data.get('last_name')
        user.is_subscribed = False
        user.save()
        return user
