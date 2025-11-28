from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description']
        labels = {
            'title': 'Tytuł bloga',
            'description': 'Opis bloga',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }