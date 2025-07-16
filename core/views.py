from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'core/main.html')
def calc(request):
    return render(request, 'core/calc.html')