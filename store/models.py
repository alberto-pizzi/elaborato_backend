from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=255)
    category_slug = models.SlugField(null=True, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.category_slug:
            self.category_slug = slugify(str(self.name))
        super().save(*args, **kwargs)



class Color(models.Model):
    color_name = models.CharField(max_length=100)

    def __str__(self):
        return self.color_name

class Size(models.Model):
    size_name = models.CharField(max_length=100)

    def __str__(self):
        return self.size_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=100)

    def __str__(self):
        return self.brand_name


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
    brand = models.ForeignKey(Brand, null=False, blank=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=False, blank=False, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, null=False,blank=False)
    variant = models.CharField(max_length=10, choices=VARIANTS, default=SIZE_COLOR)
    date_added = models.DateTimeField(auto_now_add=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDERS, default='Unisex')

    def clean(self):
        if not self.category:
            raise ValidationError('Every product must have a category.')

    def __str__(self):
        if self.brand:
            return self.brand.brand_name + " " + self.name
        else:
            return self.name



    def save(self, *args, **kwargs):
        self.clean()
        if not self.slug:
            self.slug = slugify(str(self.name))
        super().save(*args, **kwargs)

class Image(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    #product=models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    image = models.ImageField(blank=True, upload_to='static/images/')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.name:
            self.name = self.image.name
        super().save(*args, **kwargs)

class ProductVariant(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, blank=True, null=True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, blank=True, null=True)
    image_id = models.ForeignKey(Image, blank=True, null=True,on_delete=models.SET_NULL)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    quantity = models.IntegerField(default=1,null=False)
    purchased = models.PositiveIntegerField(default=0, null=False, blank=True)

    def clean(self):
        if (self.product.variant == Product.SIZE_COLOR) and not (self.color and self.size):
            raise ValidationError('This product variant should have a color and size.')
        elif (self.product.variant == Product.NONE) and (self.color or self.size):
            raise ValidationError('This product variant should not have a color or size.')
        else:
            if (self.product.variant == Product.SIZE) and self.color:
                raise ValidationError('This product variant should not have a color.')
            if self.product.variant == Product.COLOR and self.size:
                raise ValidationError('This product variant should not have a size.')
        # only for new instances
        if not self.pk:
            if ProductVariant.objects.filter(product=self.product, size=self.size, color=self.color).exists():
                raise ValidationError('Duplicate product variants could not exist')


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
        super().save(*args, **kwargs)

    def __str__(self):
        name = self.product.name + ' ' + self.product.gender
        if self.color:
            name += ' ' + self.color.color_name
        if self.size:
            name += ' ' + self.size.size_name
        return name


