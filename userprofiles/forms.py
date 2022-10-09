from django import forms
from .models import CustomerProfile


class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        exclude = ('user',)
        fields = (
            'default_mobile_number',
            'default_street_address', 'default_city', 'default_zip_code',
            'default_country', 'web_site', 'want_wishes',)
    
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
            
            'default_mobile_number': 'Mobile Number',
            'default_city': 'City',
            'default_zip_code': 'Zip Code',
            'default_street_address': 'Street Address',
            'default_country': 'Country',
            'web_site': 'web_site',
            'want_wishes': 'want_wishes',
            }
        
        self.fields['default_mobile_number'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'profile-form-input'
            self.fields[field].label = False