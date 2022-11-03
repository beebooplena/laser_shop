from django import forms
from .models import Item, Category


class ItemForm(forms.ModelForm):
    """
    A form for the edit/Add items
    This code is inspired from the
    boutique ado project, code institute.
    """
    class Meta:
        model = Item
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
