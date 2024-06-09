from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'phone', 'city', 'avatar')
    list_filter = ('id', 'city', 'phone')
    search_fields = ('id', 'email', 'city', 'phone')
