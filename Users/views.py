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
from .models import *
from .models import CartItem
from Quiz.models import QuizResults
from Quiz.models import SkinCareRoutine

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
    routine_user = SkinCareRoutine.objects.filter(username_user=request.user.username)
    
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
        'quiz_user' : quiz_user,
        'routine_user' : routine_user
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

@login_required
@require_POST
def track_product_view(request):
    try:
        data = json.loads(request.body)
        product_slug = data.get('product_slug')

        if not product_slug:
            return JsonResponse({'status': 'error', 'message': 'اسلاگ محصول ارسال نشده است'}, status=400)

        profile = request.user.profile

        if product_slug in profile.views_product:
            profile.views_product.remove(product_slug)

        profile.views_product.insert(0, product_slug)
        profile.views_product = profile.views_product[:20]
        profile.save()
        return JsonResponse({'status': 'success', 'message': 'بازدید محصول ثبت شد'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'خطای سرور: {str(e)}'}, status=500)
    
@login_required
@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_slug = data.get('product_slug')
        quantity = int(data.get('quantity', 1))

        if not product_slug:
            return JsonResponse({'status': 'error', 'message': 'اسلاگ محصول ارسال نشده است'}, status=400)

        product = Product.objects.filter(slug=product_slug).first()
        if not product:
            return JsonResponse({'status': 'error', 'message': 'محصول پیدا نشد'}, status=404)

        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({'status': 'success', 'message': f'{quantity} عدد از محصول به سبد خرید اضافه شد'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'خطای سرور: {str(e)}'}, status=500)
@login_required
def get_cart(request):
    cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    data = []
    total = 0
    for item in cart_items:
        data.append({
            'product_slug': item.product.slug,
            'name': item.product.name,
            'price': float(item.product.price),
            'quantity': item.quantity,
            'total': float(item.total_price),
        })
        total += item.total_price
    return JsonResponse({'items': data, 'total': total})

@login_required
@require_POST
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')

        if not product_id:
            return JsonResponse({'status': 'error', 'message': 'محصول انتخاب نشده است'}, status=400)

        cart = request.session.get('cart', {})

        if product_id in cart:
            del cart[product_id]
            request.session['cart'] = cart
            return JsonResponse({'status': 'success', 'message': 'محصول از سبد خرید حذف شد'})
        else:
            return JsonResponse({'status': 'info', 'message': 'محصول در سبد خرید وجود ندارد'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

@login_required
@require_POST
def checkout_cart(request):
    try:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
        if not cart_items.exists():
            return JsonResponse({'status': 'error', 'message': 'سبد خرید خالی است'}, status=400)

        total = sum(item.total_price for item in cart_items)
        profile = request.user.profile

        
        if profile.pocket < total:
            return JsonResponse({'status': 'error', 'message': 'موجودی کافی نیست'}, status=400)

       
        for item in cart_items:
            if item.quantity > item.product.stock:
                return JsonResponse({
                    'status': 'error',
                    'message': f'موجودی محصول "{item.product.name}" کافی نیست'
                }, status=400)
            item.product.stock -= item.quantity
            item.product.save()

       
        profile.pocket -= total
        profile.save()

        cart_items.delete()

        return JsonResponse({'status': 'success', 'message': 'پرداخت با موفقیت انجام شد'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)