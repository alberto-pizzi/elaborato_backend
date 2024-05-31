from django.db import models

# Create your models here.
from accounts.models import CustomUser
from store.models import Product
from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Cart ({self.user})' if self.user else f'Cart ({self.session_id})'

    def totalItems(self):
        return sum(item.quantity for item in self.cartitem_set.all())

    def totalPrice(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.quantity * item.product.price
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'