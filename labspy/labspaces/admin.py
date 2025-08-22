from django.contrib import admin
from .models import Lab, LabMembership

# Register your models here.    
admin.site.register(Lab)
admin.site.register(LabMembership)

