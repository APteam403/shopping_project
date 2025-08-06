from django.shortcuts import render, redirect

def contact_page(request):
    if request.method == 'POST':
        return redirect('signin.html')
    return render(request, 'Users/sign.html')

def signin_page(response):
    return render(response, 'Users/signin.html')
# Create your views here.