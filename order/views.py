from django.shortcuts import render

from store.models import Product, ProductVariant
from order.models import Cart, CartItem
from django.http import JsonResponse
import uuid
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
from django.contrib import messages

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        # Utente anonimo: Usa la sessione per memorizzare l'ID del carrello
        session_cart_id = request.session.get('cart_id')
        if session_cart_id:
            cart, created = Cart.objects.get_or_create(session_id=session_cart_id)
        else:
            cart = Cart.objects.create(session_id=str(uuid.uuid4()))
            request.session['cart_id'] = cart.session_id
    return cart


def add_to_cart(request):
    # TODO add "one size" feature
    if request.method == 'POST':

        prod_id = int(request.POST.get('product_id'))
        quantity = int(request.POST.get('product_qty'))
        color = int(request.POST.get('product_color'))
        size = request.POST.get('product_size')

        if size:
            size = int(size)
            product = get_object_or_404(ProductVariant, product=prod_id, size=size, color=color)
            cart = get_or_create_cart(request)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

            if created:
                cart_item.quantity = quantity
            else:
                cart_item.quantity += quantity
            cart_item.save()
            total_items = cart.total_items()
            # TODO consider anonymous user's cart

            return JsonResponse({'status': 'success', 'message': 'Product/s add to cart',
                                 'total_items': total_items,
                                 'cart_item_quantity': cart_item.quantity})

    return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'}, status=400)


def remove_from_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        product = get_object_or_404(ProductVariant, id=prod_id)
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        cart_item.delete()

        total_items = cart.total_items()
        total_price = cart.total_price()
        return JsonResponse(
            {'status': 'success', 'message': 'Prodotto aggiunto/aggiornato nel carrello.', 'total_items': total_items,
             'cart_item_quantity': cart_item.quantity, 'total_price': total_price})
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'}, status=400)



def cart_info(request):
    cart = get_or_create_cart(request)
    cart_items = CartItem.objects.filter(cart=cart).select_related('product')

    cart_products = [
        {
            'product_id': item.product.id,
            'name': item.product.title,
            'price': item.product.price,
            'quantity': item.quantity,
            'size': item.product.size.size_name,
            'color': item.product.color.color_name
        } for item in cart_items
    ]

    data_response = {
        'cart_products': cart_products,
        'total_items': cart.total_items(),
        'total_price': cart.total_price()
    }

    return data_response

def checkout(request):
    return render(request, 'order/checkout.html', cart_info(request))

def cart_overview(request):
    return render(request, 'order/cart.html', cart_info(request))
