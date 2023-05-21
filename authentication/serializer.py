from rest_framework import serializers
from authentication.models import *

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length = 255,min_length = 6)
    class Meta:
        model = User
        fields =("email","password")

class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    name = serializers.CharField(max_length = 255)
    password = serializers.CharField(max_length = 255,min_length = 6)
    class Meta:
        model = User
        fields = "__all__"