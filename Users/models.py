from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MinLengthValidator

class Profile(models.Model):
    class SkinType(models.IntegerChoices):
        DRY = 1, 'خشک'
        OILY = 2, 'چرب'
        COMBINATION = 3, 'مختلط'
        SENSITIVE = 4, 'حساس'
        NORMAL = 5, 'نرمال'

    class Gender(models.TextChoices):
        MALE = 'M', 'مرد'
        FEMALE = 'F', 'زن'
        OTHER = 'O', 'سایر'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='حساب کاربری'
    )
    
    # اطلاعات شخصی
    name = models.CharField(
        max_length=300,
        verbose_name='نام کامل',
        validators=[MinLengthValidator(3)]
    )
    
    email = models.EmailField(
        verbose_name='آدرس ایمیل',
        unique=True,
        blank=True,
        null=True
    )
    
    phone_number = models.CharField(
        max_length=15,
        verbose_name='شماره تلفن',
        blank=True,
        null=True,
        unique=True
    )
    
    birth_date = models.DateField(
        verbose_name='تاریخ تولد',
        blank=True,
        null=True
    )
    
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        verbose_name='جنسیت',
        blank=True,
        null=True
    )
    
    # اطلاعات پوست
    skin_type = models.IntegerField(
        choices=SkinType.choices,
        verbose_name='نوع پوست',
        blank=True,
        null=True
    )
    
    skin_concerns = models.JSONField(
        verbose_name='نگرانی‌های پوستی',
        default=list,
        blank=True
    )
    
    # تنظیمات و ترجیحات
    preferences = models.JSONField(
        verbose_name='ترجیحات محصولات',
        default=list,
        blank=True
    )
    
    wishlist = models.JSONField(
        verbose_name='لیست علاقه‌مندی‌ها',
        default=list,
        blank=True
    )
    
    # اطلاعات مکانی
    address = models.TextField(
        verbose_name='آدرس کامل',
        blank=True,
        null=True
    )
    
    city = models.CharField(
        max_length=100,
        verbose_name='شهر',
        blank=True,
        null=True
    )
    
    postal_code = models.CharField(
        max_length=10,
        verbose_name='کد پستی',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'پروفایل کاربر'
        verbose_name_plural = 'پروفایل‌های کاربران'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['phone_number']),
        ]

    def __str__(self):
        return f'{self.name} - {self.user.username}'

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('contact_page', kwargs={'pk': self.pk})

    @property
    def age(self):
        from datetime import date
        if self.birth_date:
            today = date.today()
            return today.year - self.birth_date.year - (
                (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
            )
        return None