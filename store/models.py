from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
class Product(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False,blank=False)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    stock = models.PositiveIntegerField(default=0, null=False,blank=True)
    purchased = models.PositiveIntegerField(default=0, null=False,blank=True)
    categories = models.ManyToManyField(Category, null=True, blank=True)
    def __str__(self):
        return self.name

