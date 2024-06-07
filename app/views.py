from django.shortcuts import render, redirect

def home(request):
    return render(request, 'home.html')

def redirect_to_api(request):
    return redirect('/api/')
