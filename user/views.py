from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import User
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
import re
    

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '').strip()
        password2 = request.POST.get('password2', '').strip()

        errors = {}

        if not username:
            errors['username'] = 'Поле имени пользователя обязательно.'
        elif not re.match(r'^[\w.@+-]+$', username):
            errors['username'] = 'Имя пользователя содержит недопустимые символы.'
        if not email:
            errors['email'] = 'Поле email обязательно.'
        elif not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            errors['email'] = 'Неверный формат email.'
        if not password:
            errors['password'] = 'Поле пароля обязательно.'
        if not password2:
            errors['password2'] = 'Поле подтверждения пароля обязательно.'
        if password and password2 and password != password2:
            errors['password2'] = 'Пароли не совпадают.'
        if password and len(password) < 8:
            errors['password'] = 'Пароль должен содержать минимум 8 символов.'
        if username and User.objects.filter(username=username).exists():
            errors['username'] = 'Это имя пользователя уже занято.'
        if email and User.objects.filter(email=email).exists():
            errors['email'] = 'Этот email уже используется.'

        if errors:
            return JsonResponse({'success': False, 'errors': errors}, status=400)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user) 
            return JsonResponse({'success': True, 'redirect_url': '/'})
        except ValidationError as e:
            errors['general'] = str(e)
            return JsonResponse({'success': False, 'errors': errors}, status=400)

    return JsonResponse({'success': False, 'errors': {'general': 'Неверный метод запроса'}}, status=405)

def login_acc(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({"success": False, "error": "Пользователь не найден"})
        
        user = authenticate(request, username=user.username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"success": True, "redirect_url": "/"}) 
        else:
            return JsonResponse({"success": False, "error": "Неверный логин или пароль"})

    return JsonResponse({"success": False, "error": "Неверный запрос"})


def logout_view(request):
    logout(request)
    return redirect('home')