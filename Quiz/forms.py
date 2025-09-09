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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['sex'].choices = [
            (QuizResults.MALE, 'مرد'),
            (QuizResults.FEMALE, 'زن'),
        ]
        
        self.fields['weather'].choices = [
            (QuizResults.DRY_AND_WARM, 'خشک و گرم'),
            (QuizResults.HUMID_AND_WARM, 'مرطوب و گرم'),
            (QuizResults.DRY_AND_COLD, 'خشک و سرد'),
            (QuizResults.HUMID_AND_COLD, 'مرطوب و سرد'),
        ]
        
        self.fields['skin_type'].choices = [
            (QuizResults.DRY, 'خشک'),
            (QuizResults.OILY, 'چرب'),
            (QuizResults.COMBINATION, 'ترکیبی'),
            (QuizResults.SENSITIVE, 'حساس'),
        ]
        
        self.fields['skin_moisture'].choices = [
            (QuizResults.DEHYDRATED, 'کم آب'),
            (QuizResults.BALANCED, 'متعادل'),
            (QuizResults.EXCESSIVELY_OILY, 'بسیار چرب'),
        ]
        
        self.fields['skin_texture'].choices = [
            (QuizResults.SMOOTH, 'صاف'),
            (QuizResults.ROUGH, 'زبر'),
        ]
        
        self.fields['skin_sensitivity'].choices = [
            (QuizResults.YES, 'بله'),
            (QuizResults.NO, 'خیر'),
        ]
        
        self.fields['sun_exposure'].choices = [
            (QuizResults.LOW, 'کم'),
            (QuizResults.MODERATE, 'متوسط'),
            (QuizResults.HIGH, 'زیاد'),
        ]
        
        self.fields['favorite_product_type'].choices = [
            (QuizResults.CREAM, 'کرم'),
            (QuizResults.OIL, 'روغن'),
            (QuizResults.GEL, 'ژل'),
            (QuizResults.SERUM, 'سرم'),
        ]