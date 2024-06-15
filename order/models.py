from django.db import models

# Create your models here.
from accounts.models import CustomUser,Address
from store.models import Product, ProductVariant
from django.conf import settings
import enum

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=50, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f'Cart ({self.user})' if self.user else f'Cart ({self.session_id})'

    def total_items(self):
        return sum(item.quantity for item in self.cartitem_set.all())

    def total_price(self):
        total = 0
        for item in self.cartitem_set.all():
            total += item.quantity * item.product.price
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price_per_product(self):
        return self.product.price * self.quantity


    def __str__(self):
        return f'{self.quantity} x {self.product.__str__()}'


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    @classmethod
    def choices(cls):
        return [(key.value, key.name.title()) for key in cls]


class Order(models.Model):
    PAYMENT_METHODS = [
        ('credit', 'Credit Card'),
        ('debit', 'Debit Card'),
        ('paypal', 'PayPal')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total_products = models.PositiveIntegerField(null=False,blank=False,editable=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2,null=False,blank=False,default=0,editable=False)
    payment_method = models.CharField(max_length=20,choices=PAYMENT_METHODS,null=False,blank=False,editable=False)
    address = models.ForeignKey(Address, on_delete=models.PROTECT,null=True,blank=True)
    status = models.CharField(max_length=20, choices=OrderStatus.choices(), default=OrderStatus.PENDING.value)

    def __str__(self):
        if self.user:
            return 'Order n.: ' + f'{self.id} x {self.user.first_name + self.user.last_name}'
        else:
            return 'Order n.: ' + f'{self.id} x {self.address.first_name_recipient + self.address.last_name_recipient}'



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
