from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import contactForm
from django.contrib import messages

def contact_page(request):
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات با موفقیت ثبت شد!')
            return redirect(reverse('index_page'))
    else:
        form = contactForm()
    
    return render(request, 'Users/sign.html', {'form': form})

def signin_page(request):
    return render(request, 'Users/signin.html')