from django import forms
from .models import QuizResults

class QuizForm(forms.ModelForm):
    class Meta:
        model = QuizResults
        fields = '__all__'
        widgets = {
            'age': forms.NumberInput(attrs={'min': 1, 'max': 120}),
            'allergic_substances': forms.Textarea(attrs={'rows': 3}),
        }