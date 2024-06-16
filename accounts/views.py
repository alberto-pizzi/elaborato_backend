from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
from .models import CustomUser, Address
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib import messages


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
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
        if len(password) >= 8:
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
            if not username_is_valid(fields['username']):
                messages.error(request, "Error: username is invalid")
            elif not email_is_valid(fields['email']):
                messages.error(request, "Error: email is invalid")
            elif not password_is_valid(password):
                messages.error(request, "Error: password is invalid")
            else:
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