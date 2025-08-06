from django.shortcuts import render, redirect
from django.urls import reverse

def contact_page(request):
    if request.method == 'POST':
        return redirect(reverse('signin_page'))
    return render(request, 'Users/sign.html')

def signin_page(request):
    return render(request, 'Users/signin.html')