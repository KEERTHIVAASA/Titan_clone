from django import forms
from .models import Review_rating

class ReviewForm(forms.ModelForm):
    model=Review_rating
    fields=['subjects','review','rating']