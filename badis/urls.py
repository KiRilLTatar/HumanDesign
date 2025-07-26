from django.urls import path
from . import views

urlpatterns = [
    path('countbudz/', views.calc_of_the_badza_card, name="calc_badz"),
]

