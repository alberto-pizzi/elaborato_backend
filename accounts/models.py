from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    address1 = models.CharField(max_length=255, blank=False)
    address2 = models.CharField(max_length=255, blank=True)
    country = models.CharField(max_length=255, blank=False)
    state = models.CharField(max_length=255, blank=False)
    zip = models.CharField(max_length=20, blank=False)
    def __str__(self):
        return self.user.username