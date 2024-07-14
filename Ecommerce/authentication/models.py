# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver


AUTH_PROVIDERS = {'google':'google'}


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        (0, 'Admin'),
        (1, 'User'),
    )
    email = models.EmailField('email address', unique=True)  # changes email to unique and blank to false
    email_verified = models.BooleanField(default=False)
    forget_password_token = models.TextField(null=True, blank=True)
    role = models.IntegerField(choices=ROLE_CHOICES, default=1)
    phone = models.CharField(max_length=15, null=False, blank=False)
    country = models.CharField(max_length=100,null=False,blank=False)
    auth_provider = models.CharField(max_length=255, blank=True, null=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class UserProfile(BaseModel):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE,related_name='user_profile')
    image = models.ImageField(upload_to='profile_pic/',null=True,blank=True)
    


@receiver(post_save, sender=CustomUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        try:
             UserProfile.objects.create(user=instance)
        except Exception as e :
            print(e)
        return True
    return False