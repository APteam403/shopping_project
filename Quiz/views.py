import json
from django.http import JsonResponse
from .prompt import prompt
from .services import get_quiz_results, get_all_products, save_routine, analyze_skin_from_image, get_image_analysis_results
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
        
        if not quiz:
            return JsonResponse({"error": "لطفاً ابتدا کوئیز را تکمیل کنید"}, status=400)
        
        # استفاده از تحلیل عکس اگر وجود دارد، در غیر این صورت از skin_concerns کوئیز
        skin_concerns = quiz.skin_concerns
        if quiz.image_analysis_data:
            skin_concerns = quiz.image_analysis_data.get("skin_concerns", quiz.skin_concerns)

        if not products:
            return JsonResponse({"error": "هیچ محصول فعالی یافت نشد"}, status=400)

        formatted_prompt = prompt.format(
            age=quiz.age,
            sex=quiz.sex,
            weather=quiz.weather,
            skin_type=quiz.skin_type,
            skin_moisture=quiz.skin_moisture,
            skin_texture=quiz.skin_texture,
            skin_sensitivity=quiz.skin_sensitivity,
            sun_exposure=quiz.sun_exposure,
            skin_concerns=skin_concerns,  # استفاده از تحلیل عکس یا کوئیز
            favorite_product_type=quiz.favorite_product_type,
            if_allergic=quiz.if_allergic,
            products=json.dumps(products, ensure_ascii=False)
        )

        api_response = send_api_to_openrouter(formatted_prompt)
        
        if "error" in api_response:
            return JsonResponse({"error": f"خطای API: {api_response['error']}"}, status=500)

        content = api_response.get('choices', [{}])[0].get('message', {}).get('content', '')
        
        try:
            parsed = json.loads(content)
            routine_text = parsed.get("routine", "")
            
            if save_routine(username, routine_text):
                # ذخیره پاسخ API در مدل QuizResults
                quiz.api_response = api_response
                quiz.save()
                
                return JsonResponse({"status": "success", "routine": routine_text})
            else:
                return JsonResponse({"error": "ذخیره روتین با خطا مواجه شد"}, status=500)
                
        except json.JSONDecodeError:
            return JsonResponse({"error": "پاسخ JSON نامعتبر از API"}, status=500)

    except Exception as e:
        return JsonResponse({"error": f"خطای سرور: {str(e)}"}, status=500)


@login_required
def analyze_skin_view(request):
    try:
        if request.method == "POST":
            # Parse JSON data
            try:
                data = json.loads(request.body)
                image_url = data.get("image_url")
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON format"}, status=400)
            
            if not image_url:
                return JsonResponse({"error": "image_url is required"}, status=400)

            result = analyze_skin_from_image(image_url)
            
            skin_concerns_text = result
            if isinstance(result, dict):
                skin_concerns_text = result.get("skin_concerns", "هیچ نگرانی پوستی شناسایی نشد")
            elif not isinstance(result, str):
                skin_concerns_text = str(result)
            
            # ذخیره نتیجه تحلیل در مدل QuizResults
            username = request.user.username
            try:
                quiz_result = models.QuizResults.objects.get(username_user=username)
                quiz_result.image_analysis_data = {"skin_concerns": skin_concerns_text}
                quiz_result.save()
            except models.QuizResults.DoesNotExist:
                return JsonResponse({"error": "لطفاً ابتدا کوئیز را تکمیل کنید"}, status=400)
            
            return JsonResponse({
                "status": "success", 
                "skin_concerns": skin_concerns_text
            })
            
        return JsonResponse({"error": "Only POST method allowed"}, status=405)
        
    except Exception as e:
        return JsonResponse({"error": f"Server error: {str(e)}"}, status=500)