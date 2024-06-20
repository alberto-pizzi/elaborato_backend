from django.shortcuts import render, redirect

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
        # Anonymous user: Use the session to store the cart ID
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
        quantity = int(request.POST.get('product_qty'))
        color = request.POST.get('product_color')
        size = request.POST.get('product_size')
        cart = get_or_create_cart(request)
        cart_item = None

        if size:
            size = int(size)
        else:
            size = None

        if color:
            color = int(color)
        else:
            color = None

        if ProductVariant.objects.filter(product=prod_id, size=size, color=color).exists():
            # FIXME warning: duplicate values
            product = ProductVariant.objects.get(product=prod_id, size=size, color=color)

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
        else:
            alert_class = "alert-danger"
            result_message = "Product selected not found"

        total_items = cart.total_items()
        return JsonResponse({'status': 'success', 'message': 'Product/s add to cart',
                             'total_items': total_items,
                             'cart_item_quantity': cart_item.quantity if cart_item else 0,
                             'result_message': result_message,
                             'alert_class': alert_class})

    alert_class = "alert-warning"
    result_message = "Select all fields, please."
    return JsonResponse({'status': 'fail', 'message': 'Invalid request method.','result_message': result_message,
                                 'alert_class': alert_class}, status=400)


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
            'name': item.product.product.brand.brand_name + " " + item.product.title,
            'price': item.product.price,
            'quantity': item.quantity,
            'size': item.product.size.size_name if item.product.size else "One size",
            'color': item.product.color.color_name if item.product.color else "One color"
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


def check_guest_checkout_required_fields(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        country = request.POST.get('country')
        state = request.POST.get('state')
        zip = request.POST.get('zip')

        if email and first_name and last_name and address1 and country and state and zip:
            return True
    return False

def checkout(request):
    cart = get_or_create_cart(request)
    data_response = {
        'user_addresses': None
    }
    user_address = None
    user_profile = None

    if request.user.is_authenticated:
        user_id = request.user.id
        user_addresses = Address.objects.filter(user=user_id).all()
        data_response['user_addresses'] = user_addresses
        user_profile = CustomUser.objects.filter(id=user_id).all().first()
        if request.method == 'POST':
            chosen_address = request.POST.get('address')
            user_address = Address.objects.filter(id=chosen_address).all().first()



    if request.method == 'POST':
        payment_method = request.POST.get('payment-method')

        if (user_address or check_guest_checkout_required_fields(request)) and payment_method:
            # check if all product in the cart are available
            for item in cart.cartitem_set.all():
                product = item.product
                if product.quantity < item.quantity:
                    messages.error(request,"Some products in the cart no longer available")
                    return redirect('order:checkout')

            # create an order

            if request.user.is_authenticated:
                order = Order(
                    user=user_profile,
                    total_products=cart.total_items(),
                    total_price=cart.total_price(),
                    shipping_nickname=user_address.nickname,
                    shipping_first_name_recipient=user_address.first_name_recipient,
                    shipping_email=user_profile.email,
                    shipping_last_name_recipient=user_address.last_name_recipient,
                    shipping_address1=user_address.address1,
                    shipping_address2=user_address.address2,
                    shipping_country=user_address.country,
                    shipping_state=user_address.state,
                    shipping_zip=user_address.zip,
                    payment_method=payment_method
                )
            else:
                email = request.POST.get('email')
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                address1 = request.POST.get('address1')
                address2 = request.POST.get('address2')
                country = request.POST.get('country')
                state = request.POST.get('state')
                zip = request.POST.get('zip')

                order = Order(
                    user=None,
                    total_products=cart.total_items(),
                    total_price=cart.total_price(),
                    shipping_nickname=first_name + ' ' + last_name + ' ' + address1,
                    shipping_first_name_recipient=first_name,
                    shipping_last_name_recipient=last_name,
                    shipping_email=email,
                    shipping_address1=address1,
                    shipping_address2=address2,
                    shipping_country=country,
                    shipping_state=state,
                    shipping_zip=zip,
                    payment_method=payment_method
                )
            order.save()

            for item in cart.cartitem_set.all():
                product = item.product

                product.quantity -= item.quantity
                product.purchased += item.quantity
                product.save()

                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity
                )

            cart.delete()
            messages.success(request, "Your order (n. " + str(order.id) + ") is placed successfully")
            return redirect('store:home')

        else:
            if not user_address:
                messages.error(request,"You have no address selected")
            if not payment_method:
                messages.error(request,"You have no payment method selected")
            return redirect('order:checkout')

    payment_methods = Order.PAYMENT_METHODS
    data_response['payment_methods'] = payment_methods

    return render(request, 'order/checkout.html', cart_info(request) | data_response)


def cart_overview(request):
    return render(request, 'order/cart.html', cart_info(request))

def orders(request):

    data_response = {
        'orders': None
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        orders = Order.objects.filter(user=user_id).all().order_by('-created_at')
        data_response['orders'] = orders



    return render(request, 'order/orders.html', cart_info(request) | data_response)


def order_detail(request, id):

    data_response = {
        'order': None
    }

    if request.user.is_authenticated:
        user_id = request.user.id
        order = Order.objects.get(id=id)
        data_response['order'] = order

        order_items = OrderItem.objects.select_related('product').filter(order=id).all()
        data_response['order_items'] = order_items

    return render(request, 'order/order-detail.html', cart_info(request) | data_response)