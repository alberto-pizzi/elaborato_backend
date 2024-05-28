from django.shortcuts import render,redirect,HttpResponse

# Create your views here.
from .models import CustomUser
from django.contrib.auth import authenticate,login
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('password')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('store:home')
        else:
            #FIXME improve error message
            return HttpResponse("Username or Password is incorrect!!!")

    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
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
            last_name=last_name,
            address1=address1,
            address2=address2,
            country=country,
            state=state,
            zip=zip
        )

        user_profile.save()

        return redirect('login')

    return render(request, 'accounts/sign-up.html')