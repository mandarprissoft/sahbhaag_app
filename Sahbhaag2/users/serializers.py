from .models import CustomUser, Center
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = CustomUser
        fields = ['last_login', 'photo', 'first_name', 'last_name', 'gender', 'age', 'username', 'password', 'contact', 'email', 'address', 'role', 'center', 'year_of_experience', 'training_type', 'discount', 'fees_paid', 'first_login', 'token']

class CenterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Center
        fields = '__all__'