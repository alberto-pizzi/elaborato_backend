from django.contrib import admin
from .models import Product,Category, Color, ProductVariant, Size, Image
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _


# Register your models here.
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Image)


class ProductVariantAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'purchased')

    list_display = ('id','prod_name','show_image','product','prod_variant','color','size','price','quantity','purchased')

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

    def prod_name(self,obj):
        if obj.product.name:
            return obj.product.name
        else:
            return "No Name"


    '''
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        product = obj.product if obj else None
        if product:
            if product.variant == Product.SIZE:
                self.exclude = ('color',)
            elif product.variant == Product.COLOR:
                self.exclude = ('size',)
            elif product.variant == Product.NONE:
                self.exclude = ('size','color')
            else:
                self.exclude = ()
        else:
            self.exclude = ()
        return form

    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        product = obj.product if obj else None
        if product:
            if product.variant == Product.SIZE:
                return [field for field in fields if field != 'color']
            elif product.variant == Product.COLOR:
                return [field for field in fields if field != 'size']
            elif product.variant == Product.NONE:
                return [field for field in fields if field != 'none']
        return fields
    '''

admin.site.register(Product)
admin.site.register(ProductVariant, ProductVariantAdmin)


