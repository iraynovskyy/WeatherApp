from django.forms import ModelForm, TextInput
from .models import City
from django.contrib.auth.models import User
from django import forms

class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}
