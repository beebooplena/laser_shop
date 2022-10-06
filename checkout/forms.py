from django import forms
from .models import Ordering


class OrderingForm(forms.ModelForm):
    class Meta:
        fields = (
            'full_name', 'email', 'mobile_number',
            'street_address', 'city', 'zip_code',
            'country',)
    
    def __init__(self, *args, **kwargs):
        """
        Adding placeholders and classes, this removes
        the auto-generated labels and also adds auto-
        focus on first field.
        This code is borrowed from code institute from
        the boutique Ado project.
        """

        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email',
            'mobile_number': 'Mobile Number',
            'city': 'City',
            'zip_code': 'Zip Code',
            'street_address': 'Street Address',
            'country': 'Country',
            }
        
        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholder[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False