from django import forms
from django.forms import ModelForm
from .models import Review_rating

class ReviewForm(forms.ModelForm):
    class Meta:
        model=Review_rating
        fields=['subject','review','rating']