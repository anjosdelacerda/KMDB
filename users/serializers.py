from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(max_length=20, validators=[UniqueValidator(queryset=User.objects.all(), message=("usuário já cadastrado"))])
    email = serializers.CharField(max_length=127, validators=[UniqueValidator(queryset=User.objects.all(), message=("email já cadastrado"))])
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    birthdate = serializers.DateField()
    bio = serializers.CharField(required=False)
    is_superuser = serializers.BooleanField(read_only=True)
    is_critic = serializers.BooleanField(required=False, default=False)
    update_at = serializers.DateTimeField(read_only=True)

    #campo estava escrito de forma errada

    def create(self, validated_data):
        new_user = User.objects.create_user(**validated_data)
        #create_user fará a hash
        return new_user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)
