from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.http import JsonResponse
from .models import User
from django.contrib.auth import login, authenticate

    

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        errors = []

        if not username or not email or not password or not password2:
            errors.append('Пожалуйста, заполните все поля.')

        if password != password2:
            errors.append('Пароли не совпадают.')

        if User.objects.filter(username=username).exists():
            errors.append('Имя пользователя уже занято.')

        if errors:
            return JsonResponse({'success': False, 'errors': errors})

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        login(request, user)

        return JsonResponse({'success': True, 'redirect_url': '/'})

    return JsonResponse({'success': False, 'errors': ['Неверный метод запроса']})

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