from django.contrib import admin
from users.models import App_Users

@admin.register(App_Users)
class AppUsersAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'is_staff')