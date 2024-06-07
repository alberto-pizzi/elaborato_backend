from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser





class CustomUser(AbstractUser):

    def __str__(self):
        return self.username

    # FIXME fix this method
    def create_custom_user(self, username, email, password, first_name, last_name):
        instance = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        instance.save()
        return instance


class Address(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
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

    # FIXME fix this method
    def create_address(self,first_name,last_name,address1,address2,country,state,zip,user=None,nickname=None):
        if nickname:
            nick = nickname
        else:
            nick = first_name + ' ' + last_name + ' ' + address1

        instance = Address(
            user=user,
            nickname=nick,
            first_name_recipient=first_name,
            last_name_recipient=last_name,
            address1=address1,
            address2=address2,
            country=country,
            state=state,
            zip=zip
        )
        instance.save()
        return instance
