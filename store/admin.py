from django.contrib import admin
from .models import Product,Category, Color, ProductVariant, Size, Image

# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(ProductVariant)
admin.site.register(Size)
admin.site.register(Image)