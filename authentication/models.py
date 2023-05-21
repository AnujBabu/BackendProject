from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,UserManager
# Create your models here.
class User(AbstractBaseUser):
    name = models.CharField(max_length=30,null=False,blank=False)
    email = models.EmailField(max_length=255,unique=True)
    username = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=13,null=False,blank=False)
    is_verified = models.BooleanField(default=False,blank=False,null=False)
    otp_email = models.CharField(max_length=6,null=True,blank=True)
    objects = UserManager()
    USERNAME_FIELD = "email"

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.pk:
            super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)