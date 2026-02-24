from rest_framework import serializers
from .models import User

class UserRegisterSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'phone_number']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']
        phone_number = validated_data.get('phone_number', None)
        user = User.objects.create_user(email=email, password=password, phone_number=phone_number)
        user.is_active = False
        user.generate_confirmation_code()
        user.save()
        return user

class UserConfirmSerializer(serializers.Serializer):
    username = serializers.CharField()
    code = serializers.CharField(max_length=6)

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
