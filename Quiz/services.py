from django.db import transaction
from .models import SkinCareRoutine, QuizResults
from Store.models import Product
from django.core.exceptions import ObjectDoesNotExist

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
                username=username,
                routine=routine_text,
            )
        return True
    except Exception as e:
        print(f"Error saving routine: {str(e)}")
        return False