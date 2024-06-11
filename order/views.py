from django.shortcuts import render

from store.models import Product, ProductVariant
from order.models import Cart, CartItem,Order,OrderItem
from accounts.models import Address, CustomUser
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
            # TODO consider anonymous user's cart
            cart_item = CartItem.objects.filter(cart=cart, product=product).first()

            # alert_class is a Bootstrap class for banner color
            alert_class = "alert-success"
            result_message = "Item/s added successfully"
            error_message = "Error: quantity selected is grower than stock, available items are: "
            if cart_item:
                if product.quantity >= (quantity + cart_item.quantity):
                    cart_item.quantity += quantity
                    cart_item.save()
                else:
                    alert_class = "alert-danger"
                    # the cart items are also counted
                    result_message = (error_message + str(product.quantity) + " of which "
                                      + str(cart_item.quantity) + " in the cart")
            elif not cart_item:
                if product.quantity >= quantity:
                    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)
                    cart_item.save()
                else:
                    alert_class = "alert-danger"
                    result_message = error_message + str(product.quantity)

            total_items = cart.total_items()
            return JsonResponse({'status': 'success', 'message': 'Product/s add to cart',
                                 'total_items': total_items,
                                 'cart_item_quantity': cart_item.quantity if cart_item else 0,
                                 'result_message': result_message,
                                 'alert_class': alert_class})

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


def get_cart_products(cart):
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

    return cart_products


def cart_info(request):
    cart = get_or_create_cart(request)
    data_response = {
        'cart_products': get_cart_products(cart),
        'total_items': cart.total_items(),
        'total_price': cart.total_price()
    }

    return data_response


def checkout(request):
    # TODO add items into order
    cart = get_or_create_cart(request)
    data_response = {
        'user_addresses': None
    }
    if request.method == 'POST':
        payment_method = request.POST.get('payment-method')
        if request.user.is_authenticated:
            user_id = request.user.id
            user_profile = CustomUser.objects.filter(id=user_id).all().first()
            user_addresses = Address.objects.filter(user=user_id).all()
            chosen_address = request.POST.get('address')

            user_address = Address.objects.filter(id=chosen_address).all().first()

            data_response['user_addresses'] = user_addresses

        else:
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            country = request.POST.get('country')
            state = request.POST.get('state')
            zip = request.POST.get('zip')
            save_user = request.POST.get('save_user')

            if save_user:
                print('Save user: yes')
                username = request.POST.get('username')
                password = request.POST.get('password')

                user_profile = CustomUser.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )

                user_profile.save()
            else:
                print('Save user: no')
                user_profile = None

            user_address = Address(
                user=user_profile,
                nickname=first_name + ' ' + last_name + ' ' + address1,
                first_name_recipient=first_name,
                last_name_recipient=last_name,
                address1=address1,
                address2=address2,
                country=country,
                state=state,
                zip=zip
            )

            user_address.save()

        order = Order(
            user=user_profile,
            total_products=cart.total_items(),
            total_price=cart.total_price(),
            address=user_address,
            payment_method=payment_method
        )
        order.save()

    payment_methods = Order.PAYMENT_METHODS
    data_response['payment_methods'] = payment_methods

    return render(request, 'order/checkout.html', cart_info(request) | data_response)


def cart_overview(request):
    return render(request, 'order/cart.html', cart_info(request))
