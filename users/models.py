import redis
from django.conf import settings

def get_redis_client():
    return redis.Redis(host=getattr(settings, 'REDIS_HOST', 'localhost'), port=getattr(settings, 'REDIS_PORT', 6379), db=0)
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
import random

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, phone_number=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, phone_number=None, **extra_fields):
        if not phone_number:
            raise ValueError('Номер телефона обязателен для суперпользователя')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        return self.create_user(email, password, phone_number, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    registration_source = models.CharField(max_length=20, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    confirmation_code = models.CharField(max_length=6, blank=True, null=True, unique=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number']

    def generate_confirmation_code(self):
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        r = get_redis_client()
        r.set(f'confirmation_code:{self.email}', code, ex=300)  # 5 минут
        return code

    def check_confirmation_code(self, code):
        r = get_redis_client()
        stored_code = r.get(f'confirmation_code:{self.email}')
        if stored_code and stored_code.decode() == code:
            r.delete(f'confirmation_code:{self.email}')
            return True
        return False
