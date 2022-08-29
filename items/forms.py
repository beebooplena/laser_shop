from django import forms
from django.forms import ModelForm

from .models import Item

class EngravedForm(forms.Form):
    class Meta:
        model = Item
        fields = ('engraved',)