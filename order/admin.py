from django.contrib import admin

# Register your models here.
from .models import Cart,CartItem,Order,OrderItem

admin.site.register(Cart)
admin.site.register(CartItem)



class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'created_at', 'total_products', 'total_price', 'payment_method')

    list_display = ('order_n', 'user','shipping_email', 'display_name', 'status', 'created_at', 'total_products', 'total_price',
                    'payment_method',
                    'display_custom_address')

    def display_custom_address(self, obj):
        return f"{obj.shipping_address1},{obj.shipping_address1}, {obj.shipping_state}, {obj.shipping_zip}, {obj.shipping_country}"

    def display_name(self,obj):
        return f"{obj.shipping_first_name_recipient} {obj.shipping_first_name_recipient}"


    def order_n(self,obj):
        return f"{obj.id}"

    display_name.short_description = 'Last/First Name Recipient'
    display_custom_address.short_description = 'Address'

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)