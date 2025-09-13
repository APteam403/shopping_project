from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist
from Store.models import Product
from .models import SkinCareRoutine, QuizResults, ImageAnalysisResults
from .api_request import send_image_to_openrouter
from .prompt import prompt_image_analysis


def get_quiz_results(username):
    try:
        return QuizResults.objects.get(username_user=username)
    except ObjectDoesNotExist:
        return None

def get_all_products():
    return list(Product.objects.filter(is_active=True).values(
        'slug', 'name', 'brand', 'description', 'category', 
        'skin_type', 'concerns_targeted', 'tags'
    ))

def save_routine(username, routine_text):
    try:
        with transaction.atomic():
            SkinCareRoutine.objects.create(
                username_user=username,
                routine=routine_text,
            )
        return True
    except Exception as e:
        print(f"Error saving routine: {str(e)}")
        return False
    
def save_image_analysis_results(username, skin_concerns):
    try:
        with transaction.atomic():
            ImageAnalysisResults.objects.create(
                username_user=username,
                skin_concerns=skin_concerns
            )
        return True
    except Exception as e:
        print(f"Error saving image analysis results: {str(e)}")
        return False

def analyze_skin_from_image(image_url):
    prompt = prompt_image_analysis
    result = send_image_to_openrouter(prompt,image_url)
    return result