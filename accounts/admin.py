from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'status', 'department', 'badge_id', 'is_staff')
    list_filter = ('role', 'status', 'department', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Digital Evidence System Fields', {
            'fields': ('role', 'status', 'department', 'badge_id', 'phone')
        }),
    )
