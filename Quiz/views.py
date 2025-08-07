from django.shortcuts import render, redirect
from .forms import QuizForm

def create_book(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = QuizForm()
    
    return render(request, 'Quiz/book.html', {'form': form})