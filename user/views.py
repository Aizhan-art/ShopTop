import random
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from .models import OTP, MyUser
from .forms import UserRegisterForms, ProfileUpdateForm

def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForms(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Вы успешно зарегистрировалитсь!')
            return redirect('index')
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(request, f'{error}')

    form = UserRegisterForms()
    return render(request, 'account/user_register.html', {'form': form})

def generate_otp_code():
    random_code =random.randint(10000, 999999)
    return random_code

def user_login_view(request):
    if request.method == 'POST':
        user_email = request.POST.get('email')
        user_password = request.POST.get('password')

        user = authenticate(request, username=user_email, password=user_password)

        if user:
            if user.is_otp:

                code = generate_otp_code()
                OTP.objects.create(user=user, code=code)

                send_mail(
                    subject='Ваш одноразовый пароль в CYBORG07',
                    message=f'Ваш OTP код:\n{code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user_email],
                    fail_silently=False,
                )
                messages.success(request, f'OTP-код отправлен вам на почту {user_email}!')
                return redirect('otp_verify', user.id)
            else:
                login(request, user)
                messages.error(request, 'Вы успешно вошли в систему!')
                return redirect('index')
        else:
            messages.error(request, 'Неверный логин или пароль')

    return render(request, 'account/user_login.html')

def user_logout_view(request):
    logout(request)
    messages.success(request,'Вы успешно вышли из системы')
    return redirect('index')

def otp_verification_view(request, user_id):
    user = get_object_or_404(MyUser, id=user_id)

    if request.method == 'POST':
        otp_code = request.POST['otp_code']

        otp = OTP.objects.filter(user=user, if_used=False, code=otp_code).last()

        if otp:
            otp.if_used=True
            login(request, user)
            messages.success(request, 'Вы успешно вошли в систему!')
            return redirect('index')

        messages.error(request, 'Неверный код!')

    return render(request, 'account/otp_verify.html')

@login_required
def toggle_2fa(request):
    user = request.user
    user.is_2fa_enabled = not user.is_2fa_enabled
    user.save()

    if user.is_2fa_enabled:
        messages.success(request, "Двухфакторная аутентификация включена!")
    else:
        messages.warning(request, "Двухфакторная аутентификация отключена!")

    return redirect('user_profile')

@login_required
def profile_edit_view(request):
    user = request.user
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("user_profile")
    else:
        form = ProfileUpdateForm(instance=user)

    return render(request, "account/profile_edit.html", {"form": form})