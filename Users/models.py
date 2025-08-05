from django.db import models

# Create your models here.

class Users_info(models.Model):
    User_Id = models.UUIDField(max_length=300, verbose_name='User-Id')
    name = models.CharField(max_length=300, verbose_name='user-name')
    email = models.EmailField(verbose_name='user-email')
    device_type = models.TextField(max_length=300, verbose_name='mobile/desktop')
    concerns = models.JSONField(default=list)
    preferences = models.JSONField(default=list)
    skin_type = models.IntegerChoices("skin_type", "dry oily combination sensitive")
    created_at = models.DateTimeField(verbose_name='created_at', auto_now_add=True, null=True)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f'{self.name}'