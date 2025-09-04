from django.contrib import admin
from .models import Lab, LabMembership, Role, LabLog

# Register your models here.    
admin.site.register(Lab)
admin.site.register(LabMembership)
admin.site.register(Role)
admin.site.register(LabLog)

