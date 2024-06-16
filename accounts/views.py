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


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        if not CustomUser.objects.filter(username=username).exists() and not CustomUser.objects.filter(email=email).exists():
            password = request.POST.get('password')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            address1 = request.POST.get('address1')
            address2 = request.POST.get('address2')
            country = request.POST.get('country')
            state = request.POST.get('state')
            zip = request.POST.get('zip')

            user_profile = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

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

            user_profile.save()
            user_address.save()

            messages.success(request, "Registered successfully! Now please log in.")
            return redirect('accounts:login')
        else:
            messages.error(request, "Error during registration. Please check the entered fields.")
            return redirect('accounts:sign-up')


    return render(request, 'accounts/sign-up.html')


def logout_view(request):
    logout(request)
    return redirect('store:home')

def check_username(request):
    username = request.POST.get('username')
    if username:
        if CustomUser.objects.filter(username=username).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Username not provided'}, status=400)

def check_email(request):
    email = request.POST.get('email')
    if email:
        if CustomUser.objects.filter(email=email).exists():
            return JsonResponse({'exists': True})
        else:
            return JsonResponse({'exists': False})
    return JsonResponse({'error': 'Username not provided'}, status=400)