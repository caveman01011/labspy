from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.
class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=8, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True, null=True, blank=True)

class CustomUserManager(BaseUserManager):
    def validate_phone_number(self, phone_number):
        if not phone_number:
            return True
        if len(phone_number) != 8:
            raise ValueError('The Phone Number field must be 8 digits')
        if not phone_number.isdigit():
            raise ValueError('The Phone Number field must be digits')
        return True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
    
        if not username:
            raise ValueError('The Username field must be set')

        if not self.validate_phone_number(extra_fields.get('phone_number')):
            raise ValueError('The Phone Number field must be 8 digits')

        username = extra_fields.get('username')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    
    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')