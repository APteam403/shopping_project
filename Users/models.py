from django.db import models

class Users_info(models.Model):
    class SkinType(models.IntegerChoices):
        DRY = 1, 'Dry'
        OILY = 2, 'Oily'
        COMBINATION = 3, 'Combination'
        SENSITIVE = 4, 'Sensitive'

    User_Id = models.UUIDField(verbose_name='User-Id')
    name = models.CharField(max_length=300, verbose_name='user-name')
    email = models.EmailField(verbose_name='user-email')
    device_type = models.CharField(max_length=300, verbose_name='mobile/desktop')
    concerns = models.JSONField(default=list)
    preferences = models.JSONField(default=list)
    skin_type = models.IntegerField(choices=SkinType.choices, verbose_name='Skin Type', null=True)
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.name}'