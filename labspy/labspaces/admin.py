from django.contrib import admin
from .models import Lab, LabMembership, Role

# Register your models here.    
admin.site.register(Lab)
admin.site.register(LabMembership)
admin.site.register(Role)

