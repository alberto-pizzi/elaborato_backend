from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from .models import CustomUser, Address
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages
import re
from django.conf import settings

from .templatetags.hashid_filters import encode_id, decode_id


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        remember_me = bool(request.POST.get('remember-me'))


        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            if user.is_active:
                login(request, user)

                if not remember_me:
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(settings.SESSION_REMEMBER_TIMEOUT)

                return redirect('store:home')
            else:
                messages.error(request, 'Sorry, your account is disabled.')
                return redirect('store:home')
        else:
            messages.error(request,"Username or Password is incorrect!")
            return redirect('accounts:login')

    return render(request, 'accounts/login.html')


def email_is_valid(email):
    if email:
        exists = CustomUser.objects.filter(email=email).exists()
        if len(email) >= 5 and ("@" in email) and ("." in email) and not exists:
            return True
    return False


def username_is_valid(username):
    if username:
        exists = CustomUser.objects.filter(username=username).exists()
        if not exists:
            return True
    return False


def password_is_valid(password):
    if password:
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_number = bool(re.search(r'\d', password))
        if has_upper and has_lower and has_number and len(password) >= 8:
            return True
    return False


def signup_view(request):
    fields = {}
    if request.method == 'POST':

        fields['username'] = request.POST.get('username')
        fields['email'] = request.POST.get('email')
        password = request.POST.get('password')
        fields['first_name'] = request.POST.get('first_name')
        fields['last_name'] = request.POST.get('last_name')
        fields['address1'] = request.POST.get('address1')
        fields['address2'] = request.POST.get('address2')
        fields['country'] = request.POST.get('country')
        fields['state'] = request.POST.get('state')
        fields['zip'] = request.POST.get('zip')

        if username_is_valid(fields['username']) and email_is_valid(fields['email']) and password_is_valid(password):
            user_profile = CustomUser.objects.create_user(
                username=fields['username'],
                email=fields['email'],
                password=password,
                first_name=fields['first_name'],
                last_name=fields['last_name']
            )

            user_address = Address(
                user=user_profile,
                nickname=fields['first_name'] + ' ' + fields['last_name'] + ' ' + fields['address1'],
                first_name_recipient=fields['first_name'],
                last_name_recipient=fields['last_name'],
                address1=fields['address1'],
                address2=fields['address2'],
                country=fields['country'],
                state=fields['state'],
                zip=fields['zip']
            )

            user_profile.save()
            user_address.save()

            messages.success(request, "Registered successfully! Now please log in.")
            return redirect('accounts:login')
        else:
            found_invalid = False
            if not username_is_valid(fields['username']):
                found_invalid = True
                messages.error(request, "Error: username is invalid")
            if not email_is_valid(fields['email']):
                found_invalid = True
                messages.error(request, "Error: email is invalid")
            if not password_is_valid(password):
                found_invalid = True
                messages.error(request, "Error: password is invalid")
            if not found_invalid:
                messages.error(request, "Error during registration. Please check the entered fields.")
            return render(request, 'accounts/sign-up.html',fields)

    return render(request, 'accounts/sign-up.html',fields)


def logout_view(request):
    logout(request)
    return redirect('store:home')

def check_username(request):
    username = request.POST.get('username')
    if username:
        if not username_is_valid(username):
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Username not provided'}, status=400)

def check_email(request):
    email = request.POST.get('email')
    if email:
        if not email_is_valid(email):
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Username not provided'}, status=400)

def profile(request):

    data_response = {
        'addresses': None

    }

    if request.user.is_authenticated:
        user_id = request.user.id
        addresses = Address.objects.filter(user=user_id).all()
        data_response['addresses'] = addresses
        encrypted_addresses = []
        for address in addresses:
            encrypted_id = encode_id(address.id)
            encrypted_addresses.append({
                'address': address,
                'encrypted_id': encrypted_id
            })

        data_response['addresses'] = encrypted_addresses

    return render(request, 'accounts/profile.html',  data_response)



def add_address(request):

    data_response = {
        'addresses': None
    }

    fields = {}

    if request.user.is_authenticated:
        user_id = request.user.id
        addresses = Address.objects.filter(user=user_id).all()
        data_response['addresses'] = addresses

        if request.method == 'POST':
            fields['address_nick'] = request.POST.get('address_nick')
            fields['first_name'] = request.POST.get('first_name')
            fields['last_name'] = request.POST.get('last_name')
            fields['address1'] = request.POST.get('address1')
            fields['address2'] = request.POST.get('address2')
            fields['country'] = request.POST.get('country')
            fields['state'] = request.POST.get('state')
            fields['zip'] = request.POST.get('zip')

            if fields['address_nick']:
                nick = fields['address_nick']
            else:
                nick = fields['first_name'] + ' ' + fields['last_name'] + ' ' + fields['address1']

            if fields['first_name'] and fields['last_name'] and fields['address1'] and fields['country'] and fields['state'] and fields['zip']:
                user_profile = CustomUser.objects.get(id=user_id);
                user_address = Address(
                    user=user_profile,
                    nickname=nick,
                    first_name_recipient=fields['first_name'],
                    last_name_recipient=fields['last_name'],
                    address1=fields['address1'],
                    address2=fields['address2'],
                    country=fields['country'],
                    state=fields['state'],
                    zip=fields['zip']
                )

                user_address.save()

                messages.success(request, "Your address has been added successfully!")
                return redirect('accounts:profile')
            else:
                messages.error(request, "Error adding your address, please try again.")
                return redirect('accounts:add-address')
    else:
        messages.error(request, "Error: you must be logged in to add an address.")

    return render(request, 'accounts/add-address.html',  data_response)


def edit_address(request,encoded_id):
    data_response = {
        'can_edit': False
    }
    fields = {}

    if request.user.is_authenticated:

        decoded_id = decode_id(encoded_id)

        user_profile = CustomUser.objects.get(id=request.user.id)

        address = Address.objects.get(id=decoded_id, user=user_profile)

        if user_profile and address:
            data_response['can_edit'] = True

        fields['address_nick'] = address.nickname
        fields['first_name'] = address.first_name_recipient
        fields['last_name'] = address.last_name_recipient
        fields['address1'] = address.address1
        fields['address2'] = address.address2
        fields['country'] = address.country
        fields['state'] = address.state
        fields['zip'] = address.zip

    return render(request, 'accounts/edit-address.html', data_response | fields)


def delete_address(request,encoded_id):
    data_response = {
        'can_edit': False
    }


    if request.user.is_authenticated:

        decoded_id = decode_id(encoded_id)

        user_profile = CustomUser.objects.get(id=request.user.id)
        address = Address.objects.get(id=decoded_id, user=user_profile)
        success_message = 'Address ' + str(address.nickname) + ' deleted successfully'

        if user_profile and address:
            address.delete()

            messages.success(request, success_message)
            return redirect('accounts:profile')

    messages.error(request, 'Deletion failed ')
    return redirect('accounts:profile')