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
        fields = ['title', 'description', 'existing_category', 'new_category']
        labels = {
            'title': 'Tytuł bloga',
            'description': 'Opis bloga',
        }
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

    def clean(self):
        cleaned = super().clean()
        existing = cleaned.get("existing_category")
        new = cleaned.get("new_category")

        # Nie można wybrać i wpisać jednocześnie
        if existing and new:
            self.add_error("new_category", "Nie możesz wybrać i wpisać kategorii jednocześnie.")

        # Jeśli wpisano nową kategorię, sprawdzamy czy już istnieje
        if new:
            if BlogCategory.objects.filter(name__iexact=new.strip()).exists():
                self.add_error("new_category", "Taka kategoria już istnieje — wybierz ją z listy.")

        return cleaned
