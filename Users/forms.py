# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'name', 'phone_number', 'birth_date', 'gender',
            'skin_type', 'address', 'city', 'postal_code', 'skin_concerns'
        ]
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone_number', 'birth_date', 'gender',
            'skin_type', 'address', 'city', 'postal_code', 'skin_concerns'
        ]
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '09123456789'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'skin_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'skin_concerns': forms.Textarea(attrs={'class': 'form-select', 'rows':3}),
        }
        labels = {
            'phone_number': 'شماره موبایل',
            'birth_date': 'تاریخ تولد',
            'gender': 'جنسیت',
            'skin_type': 'نوع پوست',
            'address': 'آدرس کامل',
            'city': 'شهر',
            'postal_code': 'کد پستی',
            'skin_concerns': 'نگرانی‌های پوستی',
        }