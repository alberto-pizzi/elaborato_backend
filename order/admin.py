from django.contrib import admin

# Register your models here.
from .models import Cart,CartItem,Order,PaymentMethod,OrderItem

admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(PaymentMethod)


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'created_at', 'total_products', 'total_price', 'payment_method')

    list_display = ('id', 'user', 'status', 'created_at', 'total_products', 'total_price', 'payment_method',
                    'display_custom_address')

    def display_custom_address(self, obj):
        return f"{obj.address.address1}, {obj.address.state}, {obj.address.zip}, {obj.address.country}"


admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)