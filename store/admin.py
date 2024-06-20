from django.contrib import admin
from .models import Product,Category, Color, ProductVariant, Size, Image,Brand
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'category_slug')

    fieldsets = (
        (_('Category Info'), {'fields': ('name',)}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name',),
        }),
    )

class ProductAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'slug')

    list_display = ('id','brand','name','category','base_price','variant','gender')



class ProductVariantAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'purchased')

    list_display = ('id','show_image','product','prod_gender','prod_variant','color','size','price','quantity','purchased')

    fieldsets = (
        (_('Product Variant Info'), {'fields': ('image_id','product','color','size','price','quantity')}),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('image_id','product','color','size','price','quantity'),
        }),
    )

    def show_image(self, obj):
        if obj.image_id and obj.image_id.image:
            return format_html('<img src="{}" width="50px" height="auto" />', obj.image_id.image.url)
        return "No Image"
    show_image.short_description = 'Image'

    def prod_variant(self, obj):
        return f"{obj.product.variant}"

    prod_variant.short_description = 'Variant Type'

    def prod_gender(self, obj):
        if obj.product.gender:
            return obj.product.gender
        else:
            return "Gender not found"




admin.site.register(Product,ProductAdmin)
admin.site.register(ProductVariant, ProductVariantAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Image)
admin.site.register(Brand)

