from django import forms
from .models import Users_info

class contactForm(forms.ModelForm):
    class Meta:
        model = Users_info
        fields = '__all__'