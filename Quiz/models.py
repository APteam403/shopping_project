from django.db import models

class QuizResults(models.Model):
    
    MALE = 'Male'
    FEMALE = 'Female'
    SEX_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]

    DRY_AND_WARM = 'Dry and warm'
    HUMID_AND_WARM = 'Humid and warm'
    DRY_AND_COLD = 'Dry and cold'
    HUMID_AND_COLD = 'Humid and cold'
    WEATHER_CHOICES = [
        (DRY_AND_WARM, 'Dry and warm'),
        (HUMID_AND_WARM, 'Humid and warm'),
        (DRY_AND_COLD, 'Dry and cold'),
        (HUMID_AND_COLD, 'Humid and cold')
    ]

    DRY = 'Dry'
    OILY = 'Oily'
    COMBINATION = 'Combination'
    SENSITIVE = 'Sensitive'
    SKIN_TYPE_CHOICES = [
        (DRY, 'Dry'),
        (OILY, 'Oily'),
        (COMBINATION, 'Combination'),
        (SENSITIVE, 'Sensitive')
    ]

    DEHYDRATED = 'Dehydrated'
    BALANCED = 'Balanced'
    EXCESSIVELY_OILY = 'Excessively oily'
    SKIN_MOISTURE_CHOICES = [
        (DEHYDRATED, 'Dehydrated'),
        (BALANCED, 'Balanced'),
        (EXCESSIVELY_OILY, 'Excessively oily')
    ]

    SMOOTH = 'Smooth'
    ROUGH = 'Rough'
    SKIN_TEXTURE_CHOICES = [
        (SMOOTH, 'Smooth'),
        (ROUGH, 'Rough')
    ]

    YES = 'Yes'
    NO = 'No'
    YES_OR_NO_CHOICE = [
        (YES, 'Yes'),
        (NO, 'No')
    ]

    LOW = 'Low'
    MODERATE = 'Moderate'
    HIGH = 'High'
    SUN_EXPOSURE_CHOICES = [
        (LOW, 'Low'),
        (MODERATE, 'Moderate'),
        (HIGH, 'High')
    ]

    CREAM = 'Cream'
    OIL = 'Oil'
    GEL = 'Gel'
    SERUM = 'Serum'
    FAVORITE_PRODUCT_TYPE_CHOICES = [
        (CREAM, 'Cream'),
        (OIL, 'Oil'),
        (GEL, 'Gel'),
        (SERUM, 'Serum')
    ]
    username_user = models.CharField(max_length=300, default="", blank=True)
    full_name = models.CharField(max_length=300, default="")
    age = models.PositiveSmallIntegerField()
    sex = models.CharField(max_length=6, choices=SEX_CHOICES, default=MALE)
    weather = models.CharField(max_length=14, choices=WEATHER_CHOICES, default=DRY_AND_WARM)
    skin_type = models.CharField(max_length=11, choices=SKIN_TYPE_CHOICES, default=DRY)
    skin_moisture = models.CharField(max_length=16, choices=SKIN_MOISTURE_CHOICES, default=DEHYDRATED)
    skin_texture = models.CharField(max_length=6, choices=SKIN_TEXTURE_CHOICES, default=SMOOTH)
    skin_sensitivity = models.CharField(max_length=3, choices=YES_OR_NO_CHOICE, default=NO)
    skin_concerns = models.TextField(default="", blank=True)
    sun_exposure = models.CharField(max_length=8, choices=SUN_EXPOSURE_CHOICES, default=MODERATE)
    favorite_product_type = models.CharField(max_length=5, choices=FAVORITE_PRODUCT_TYPE_CHOICES, default=CREAM)
    if_allergic = models.TextField(blank=True)

    def __str__(self):
        return f'{self.full_name}'
    
class ImageAnalysisResults(models.Model):
    username_user = models.CharField(max_length=300, default="unknown")
    skin_concerns = models.TextField(default="", blank=True)

class SkinCareRoutine(models.Model):
    username_user = models.CharField(max_length=300, default="unknown")
    routine = models.TextField()