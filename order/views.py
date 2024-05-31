from django.shortcuts import render

from store.models import Product
from order.models import Cart,CartItem
from django.http import JsonResponse
import uuid
from django.shortcuts import get_object_or_404


# Create your views here.
from django.contrib import messages
def checkout(request):
    return render(request, 'order/checkout.html')


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
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=prod_id)
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        total_items = cart.total_items()
        print("ID: ", prod_id," Quantity: ",cart_item.quantity)
        # TODO consider anonymous user's cart
        return JsonResponse({'status': 'success', 'message': 'Prodotto aggiunto/aggiornato nel carrello.',
                             'total_items': total_items, 'cart_item_quantity': cart_item.quantity})
    print("Invalid request method")
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method.'}, status=400)


def remove_from_cart(request):
    if request.method == 'POST':
        prod_id = int(request.POST.get('product_id'))
        product = get_object_or_404(Product, id=prod_id)
        cart = get_or_create_cart(request)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        cart_item.quantity -= 1
        cart_item.save()
        if cart_item.quantity <= 0:
            cart_item.delete()

        total_items = cart.total_items()
        return JsonResponse(
            {'status': 'success', 'message': 'Prodotto aggiunto/aggiornato nel carrello.', 'total_items': total_items,
             'cart_item_quantity': cart_item.quantity})