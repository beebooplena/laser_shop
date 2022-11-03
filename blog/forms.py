from django import forms
from .models import BlogPost


class BlogForm(forms.ModelForm):
    """
    A form for the blog
    """
    class Meta:
        model = BlogPost
        fields = '__all__'
