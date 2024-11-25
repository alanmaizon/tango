from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Product

class CustomUserCreationForm(UserCreationForm):
    phone_number = forms.CharField(required=False, max_length=15)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone_number', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['custom_name', 'chain_type', 'chain_length', 'material', 'font_style']