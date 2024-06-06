from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser





class CustomUser(AbstractUser):

    def __str__(self):
        return self.username


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, blank=True)
    nickname = models.CharField(max_length=255, blank=True, null=False)
    first_name_recipient = models.CharField(max_length=255, blank=True, null=True)
    last_name_recipient = models.CharField(max_length=255, blank=True, null=True)
    address1 = models.CharField(max_length=255, blank=False, null=False)
    address2 = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, blank=False, null=False)
    state = models.CharField(max_length=255, blank=False, null=False)
    zip = models.CharField(max_length=20, blank=False, null=False)

    def __str__(self):
        return self.nickname

