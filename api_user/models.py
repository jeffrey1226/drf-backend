from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver


class User(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(max_length=400)
    password = models.CharField(max_length=400)
    profile_name = models.CharField(max_length=400, blank=True, null=True)
    bio = models.CharField(max_length=400, blank=True, null=True)
    is_direct = models.BooleanField(default=False, blank=True, null=True)
    avatar = models.ImageField('avatar', blank=True, null=True)

    class Meta:
        db_table = 'auth_user'


@receiver(models.signals.post_delete, sender=User)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.avatar:
        instance.avatar.delete(False)


class ResetPassword(models.Model):
    user_id = models.IntegerField(default=0, null=True)
    email = models.EmailField(blank=True, null=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        db_table = 'reset_password'
