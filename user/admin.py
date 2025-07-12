from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    User = get_user_model()
    list_display = [field.name for field in User._meta.get_fields() if not field.many_to_many and not field.one_to_many]