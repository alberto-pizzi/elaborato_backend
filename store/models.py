from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    category_slug = models.SlugField(null=False, unique=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name

class Size(models.Model):
    size_name = models.CharField(max_length=100)

    def __str__(self):
        return self.size_name



class Product(models.Model):
    NONE = 'None'
    SIZE = 'Size'
    COLOR = 'Color'
    SIZE_COLOR = 'Size-Color'
    VARIANTS = (
        (NONE, 'None'),
        (SIZE, 'Size'),
        (COLOR, 'Color'),
        (SIZE_COLOR, 'Size-Color'),
    )
    GENDERS = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Unisex', 'Unisex')
    )

    name = models.CharField(max_length=255, null=False, blank=False)
    slug = models.SlugField(null=False, unique=True)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=False,blank=False)
    variant = models.CharField(max_length=10, choices=VARIANTS, default=SIZE_COLOR)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, default='Unisex')

    def __str__(self):
        return self.name

class Image(models.Model):
    name = models.CharField(max_length=50, blank=True)
    product=models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(blank=True, upload_to='static/images/')

    def __str__(self):
        return self.name

class ProductVariant(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.ForeignKey(Image, blank=True, null=True,on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1,null=False)
    purchased = models.PositiveIntegerField(default=0, null=False, blank=True)

    def clean(self):
        if (self.product.variant == Product.NONE) and (self.color or self.size):
            raise ValidationError('This product variant should not have a color or size.')
        else:
            if (self.product.variant == Product.SIZE) and self.color:
                raise ValidationError('This product variant should not have a color.')
            if self.product.variant == Product.COLOR and self.size:
                raise ValidationError('This product variant should not have a size.')

    def save(self, *args, **kwargs):
        self.clean()
        if not self.title:
            self.title = self.product.name
            if self.color and (self.product.variant == self.product.COLOR or self.product.variant == self.product.SIZE_COLOR):
                self.title += " " + self.color.color_name
            if self.size and (self.product.variant == self.product.SIZE or self.product.variant == self.product.SIZE_COLOR):
                self.title += " " + self.size.size_name
        if not self.price:
            self.price = self.product.base_price
        print(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.product.name + ' ' + self.product.gender
        if self.color:
            name += ' ' + self.color.color_name
        if self.size:
            name += ' ' + self.size.size_name
        return name


