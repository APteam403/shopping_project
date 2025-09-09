import json
from django.http import JsonResponse
from .prompt import prompt
from .services import get_quiz_results, get_all_products, save_routine
from .api_request import send_api_to_openrouter
from django.shortcuts import render, redirect
from .forms import QuizForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth import login, authenticate
from . import models
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

def create_book(request):
    if not request.user.is_authenticated:
        return render(request, 'login_page')
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.username_user = request.user.username
            quiz.save()
            messages.success(request, 'اطلاعات با موفقیت ثبت شد!')
            return redirect(reverse('index_page'))
    else:
        form = QuizForm()
    
    return render(request, 'Quiz/book.html', {'form': form})

@login_required
def generate_and_save_routine_view(request):
    try:
        username = request.user.username
        quiz = get_quiz_results(username)
        products = get_all_products()
        
        if not quiz or not products:
            return JsonResponse({"error": "Missing quiz data or products"}, status=400)

        formatted_prompt = prompt.format(
            age=quiz.age,
            sex=quiz.sex,
            weather=quiz.weather,
            skin_type=quiz.skin_type,
            skin_moisture=quiz.skin_moisture,
            skin_texture=quiz.skin_texture,
            skin_sensitivity=quiz.skin_sensitivity,
            sun_exposure=quiz.sun_exposure,
            favorite_product_type=quiz.favorite_product_type,
            if_allergic=quiz.if_allergic,
            products=json.dumps(products, ensure_ascii=False)
        )

        api_response = send_api_to_openrouter(formatted_prompt)
        
        if "error" in api_response:
            return JsonResponse({"error": f"API Error: {api_response['error']}"}, status=500)

        content = api_response['choices'][0]['message']['content']
        parsed = json.loads(content)
        
        if not parsed.get("routine"):
            raise ValueError("Invalid routine format")

        if save_routine(username, parsed["routine"]):
            return JsonResponse({"status": "success", "data": parsed})
        
        return JsonResponse({"error": "Failed to save routine"}, status=500)

    except Exception as e:
        return JsonResponse({"error": f"Server Error: {str(e)}"}, status=500)