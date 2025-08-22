from django.db import models
from users.models import CustomUser
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

import random
import string

# Create your models here.

class Lab(models.Model):
    
    code = models.CharField(max_length=6, unique=True, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True, max_length=1024)
    contact_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_code(self):
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def save(self, *args, **kwargs):
        if self.contact_email:        
            try:
                validate_email(self.contact_email)
            except ValidationError:
                raise ValidationError("Please enter a valid email address")
        self.code = self.generate_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class LabMembership(models.Model):
    ROLE_CHOICES = [
        ('pending', 'Pending'),
        ('owner', 'Owner'),
        ('manager', 'Manager'),
        ('researcher', 'Researcher'),
        ('guest', 'Guest'),
    ]
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.CharField(max_length=64, choices=ROLE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.lab.name} - {self.role}"
    

