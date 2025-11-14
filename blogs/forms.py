from django import forms
from .models import Post
from .models import Blog

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        labels = {
            'title': 'Tytuł',
            'content': 'Treść',
        }

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