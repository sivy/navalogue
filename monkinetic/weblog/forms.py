from django import forms
from .models import Entry


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            "created",
            "title",
            "slug",
            "body",
            "summary",
            "image",
            "card_image",
            "tags",
        ]
        widgets = {
            "created": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "tags": forms.SelectMultiple(),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = [
            "title",
            "body",
            "image",
            "tags",
        ]
        widgets = {
            "tags": forms.SelectMultiple(),
        }
