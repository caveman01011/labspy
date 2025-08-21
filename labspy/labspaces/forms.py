from django import forms    

from .models import Lab

class LabCreationForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ['name', 'description', 'contact_email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'e.g. "Molecular Biology Group"'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Describe your lab 1-2 lines!'})
        self.fields['contact_email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'e.g.: "labmanager@example.com"'})
        self.fields['name'].label = 'Labspace Name'
        self.fields['description'].label = 'Lab Description (optional)'
        self.fields['contact_email'].label = 'Labspace Contact Email (optional)'