from django import forms    

from .models import Lab, Role

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

class LabJoinForm(forms.Form):
    code = forms.CharField(
        max_length=6,
        min_length=6,
        help_text="Enter the lab's 6 character alphanumeric code",
        label="Labspace Code",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter the 6-character code',
            'autocomplete': 'off',
            'inputmode': 'text',
            'pattern': '[A-Za-z0-9]{6}',
        })
    )

    def clean_code(self):
        code = self.cleaned_data['code']
        if not code.isalnum() or len(code) != 6:
            raise forms.ValidationError("Code must be exactly 6 alphanumeric characters (letters and numbers only).")
        return code

class UserManagementSearchForm(forms.Form):
    username = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by username...',
        }),
        label='Username'
    )
    
    first_name = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by first name...',
        }),
        label='First Name'
    )
    
    last_name = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by last name...',
        }),
        label='Last Name'
    )
    
    role = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'All Roles'),
            ('owner', 'Owner'),
            ('admin', 'Admin'),
            ('member', 'Member'),
            ('manager', 'Manager'),
            ('researcher', 'Researcher'),
            ('guest', 'Guest'),
        ],
        widget=forms.Select(attrs={
            'class': 'form-select',
        }),
        label='Role'
    )