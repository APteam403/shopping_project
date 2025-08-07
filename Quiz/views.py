from django.shortcuts import render, redirect
from .forms import QuizForm
from django.contrib import messages
from django.urls import reverse

def create_book(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات با موفقیت ثبت شد!')
            return redirect(reverse('index_page'))
    else:
        form = QuizForm()
    
    return render(request, 'Quiz/book.html', {'form': form})