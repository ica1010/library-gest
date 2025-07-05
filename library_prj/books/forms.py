from django import forms
from .models import Book, Category, Genre

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            "title", "summary", "isbn", "publication_date", "pages", "language", "stock", "image", "categories", "genres"
        ]
        widgets = {
            "categories": forms.CheckboxSelectMultiple(),
            "genres": forms.CheckboxSelectMultiple(),
            "publication_date": forms.DateInput(attrs={"type": "date"}),
            "summary": forms.Textarea(attrs={"rows": 3}),
        } 