from django.shortcuts import render, redirect

# Create your views here.

def index(request):
    return render(request, 'store/index.html')

def goto_login(request):
    return redirect('accounts:login')