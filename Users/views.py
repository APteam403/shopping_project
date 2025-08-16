from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm, ProfileForm, UserUpdateForm
from django.contrib.auth import logout
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from Store.models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from Quiz.models import QuizResults

def register_view(request):
    if request.method == 'POST':
        user_form = CustomUserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.email = user.email
            profile.save()

            login(request, user)
            return redirect('index_page')

    else:
        user_form = CustomUserCreationForm()
        profile_form = ProfileForm()

    return render(request, 'Users/sign.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'username12' : f'نام کاربری :',
        'username13' : f'ایمیل :',
        'username14' : f'رمز عبور :',
        'username15' : f'تائید رمز عبور :',
    })

def login_view(request):
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index_page')
        else:
            return render(request, 'Users/signin.html', {'error_message': 'Invalid username or password.'})
    else:
        return render(request, 'Users/signin.html')

def logout_view(request):
    logout(request)
    return redirect('index_page')

def dashboard(request):
    if not request.user.is_authenticated:
        return render(request, 'Users/signin.html')
    
    profile, created = Profile.objects.get_or_create(user=request.user)

    quiz_user = QuizResults.objects.filter(username_user=request.user.username)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'اطلاعات شما با موفقیت به‌روزرسانی شد.')
            return redirect('dashboard')
    else:
        form = UserUpdateForm(instance=profile)
    
    context = {
        'form': form,
        'profile': profile,
        'quiz_user' : quiz_user
    }
    return render(request, 'Users/dashboard.html', context)
@login_required
@require_POST
def add_to_favorites(request):
    try:
        data = json.loads(request.body)
        product_slug = data.get('product_slug')
        
        if not product_slug:
            return JsonResponse({
                'status': 'error',
                'message': 'اسلاگ محصول ارسال نشده است'
            }, status=400)

        profile = request.user.profile
        if product_slug not in profile.preferences:
            profile.preferences.append(product_slug)
            profile.save()
            return JsonResponse({
                'status': 'success',
                'message': 'محصول به علاقه‌مندی‌ها اضافه شد'
            })
        
        return JsonResponse({
            'status': 'info',
            'message': 'این محصول قبلاً در علاقه‌مندی‌ها وجود دارد'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'خطای سرور: {str(e)}'
        }, status=500)

@login_required
@require_POST
def add_to_wishlist(request):
    try:
        data = json.loads(request.body)
        product_slug = data.get('product_slug')
        
        if not product_slug:
            return JsonResponse({
                'status': 'error',
                'message': 'اسلاگ محصول ارسال نشده است'
            }, status=400)

        profile = request.user.profile
        if product_slug not in profile.wishlist:
            profile.wishlist.append(product_slug)
            profile.save()
            return JsonResponse({
                'status': 'success',
                'message': 'محصول به آرزومندی ها اضافه شد'
            })
        
        return JsonResponse({
            'status': 'info',
            'message': 'این محصول قبلا در آرزومندی ها اضافه شده است'
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'خطای سرور: {str(e)}'
        }, status=500)