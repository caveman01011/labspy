from django.db import models

# Create your models here.

class Equipment(models.Model):
    CATEGORY_CHOICES = [
        ("general", "General Lab Equipment"),
        ("glassware", "Glassware & Plastics"),
        ("chemicals", "Chemicals & Reagents"),
        ("consumables", "Consumables"),
        ("electronics", "Electronics & Instruments"),
        ("safety", "Safety & Storage"),
        ("office", "Office & Miscellaneous"),
        ("other", "Other"),
    ]

    STATUS_CHOICES=[
        ("available", "Available"),
        ("in_use", "In Use"),
        ("maintenance", "Under Maintenance"),
        ("broken", "Broken"),
    ]
    
    name = models.CharField(max_length=101)
    category = models.CharField(max_length=64,choices=CATEGORY_CHOICES, default="other")
    quantity = models.PositiveIntegerField(default=0)
    location = models.CharField(max_length=64)
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="available")
    description = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.location} - {self.status}"


