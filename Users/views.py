from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm, ProfileForm

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

            # لاگین خودکار
            login(request, user)
            return redirect('contact_page')

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
