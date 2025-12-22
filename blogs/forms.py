from django import forms
from .models import Blog, BlogCategory

class BlogForm(forms.ModelForm):
    existing_category = forms.ModelChoiceField(
        queryset=BlogCategory.objects.all(),
        required=False,
        label="Wybierz kategorię"
    )
    new_category = forms.CharField(
        required=False,
        label="Lub wpisz nową kategorię"
    )

    class Meta:
        model = Blog
        fields = ['title', 'description', 'existing_category', 'new_category', 'image']
        labels = {
            'title': 'Tytuł bloga',
            'description': 'Opis bloga',
            'image': 'Zdjęcie bloga'
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        blog = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        # Ustawiamy kategorię przy edycji
        if blog and blog.category:
            self.fields['existing_category'].initial = blog.category

    def clean(self):
        cleaned = super().clean()
        existing = cleaned.get("existing_category")
        new = cleaned.get("new_category")

        if existing and new:
            self.add_error("new_category", "Nie możesz wybrać i wpisać kategorii jednocześnie.")

        if new:
            if BlogCategory.objects.filter(name__iexact=new.strip()).exists():
                self.add_error("new_category", "Taka kategoria już istnieje — wybierz ją z listy.")

        return cleaned
