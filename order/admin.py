from django.contrib import admin

# Register your models here.
from .models import Cart,CartItem,Order,OrderItem
from django.urls import reverse
from django.utils.html import format_html

admin.site.register(Cart)
admin.site.register(CartItem)



class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('id', 'user', 'created_at', 'total_products', 'total_price', 'payment_method')

    list_display = ('order_n', 'user','shipping_email', 'display_name', 'status', 'created_at', 'total_products', 'total_price',
                    'payment_method',
                    'display_custom_address','get_order_items_link')

    list_display_links = ('order_n', 'get_order_items_link',)



    def get_order_items_link(self, obj):
        url = reverse('admin:order_orderitem_changelist') + f'?order_id={obj.id}'
        return format_html('<a href="{}">View Order Items</a>', url)

    get_order_items_link.short_description = 'Order Items'

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