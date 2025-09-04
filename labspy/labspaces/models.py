from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db.models import Q


from users.models import CustomUser

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

    def has_pending_requests(self):
        """
        Returns True if there are any pending join requests for this lab.
        """
        try:
            pending_role = Role.objects.get(name='pending', is_default=True, lab__isnull=True)
            return LabMembership.objects.filter(lab=self, role=pending_role).exists()
        except Role.DoesNotExist:
            return False
    
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

class Role(models.Model):
    """
    Roles define the permissions of each member in a lab.
    The field (is_default) is set to True only for roles that 
    are included by default in every lab and not associated 
    with one lab.
    """
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=255)
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE, null=True, blank=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        unique_together = ('lab', 'name', 'is_default')

    def __str__(self):
        return self.name


class LabMembership(models.Model):
    """
    Membership of a user in a lab, with their assigned role.
    """
    lab = models.ForeignKey(Lab, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, default=1, on_delete=models.SET_DEFAULT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('lab', 'user')

    def __str__(self):
        return f"{self.user.username} - {self.lab.name} - {self.role}"
    

