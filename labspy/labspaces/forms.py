from django import forms    

from .models import Lab

class LabCreationForm(forms.ModelForm):
    class Meta:
        model = Lab
        fields = ['name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})