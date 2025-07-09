from django.db import models
from user.models import User

class CelestialStem(models.Model):  
    name = models.CharField("Название", max_length=10)  
    element = models.CharField("Элемент", max_length=10) 
    yin_yang = models.BooleanField("Инь/Ян")  

class EarthlyBranch(models.Model):  
    name = models.CharField("Название", max_length=10) 
    element = models.CharField("Элемент", max_length=10)
    animal = models.CharField("Животное", max_length=20)

class BaziCalculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField("Дата расчёта", auto_now_add=True)
    
    birth_datetime = models.DateTimeField("Дата/время рождения")
    birth_place = models.CharField("Место рождения", max_length=100)
    gender = models.CharField("Пол", max_length=1, choices=[('M', 'Мужской'), ('F', 'Женский')])
    
    year_stem = models.ForeignKey(CelestialStem, related_name='year_calc', on_delete=models.PROTECT)
    year_branch = models.ForeignKey(EarthlyBranch, related_name='year_calc', on_delete=models.PROTECT)
    
    month_stem = models.ForeignKey(CelestialStem, related_name='month_calc', on_delete=models.PROTECT)
    month_branch = models.ForeignKey(EarthlyBranch, related_name='month_calc', on_delete=models.PROTECT)
    
    day_stem = models.ForeignKey(CelestialStem, related_name='day_calc', on_delete=models.PROTECT)
    day_branch = models.ForeignKey(EarthlyBranch, related_name='day_calc', on_delete=models.PROTECT)
    
    hour_stem = models.ForeignKey(CelestialStem, related_name='hour_calc', on_delete=models.PROTECT)
    hour_branch = models.ForeignKey(EarthlyBranch, related_name='hour_calc', on_delete=models.PROTECT)
    