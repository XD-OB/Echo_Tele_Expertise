from django.contrib import admin
from .models import User

class   UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'last_name', 'first_name', 'speciality', 'city')
    list_display_links = ('email', )
    list_filter = ('is_staff', 'is_active', 'is_enable_mail', 'online_status', 'city', 'speciality')
    search_fields = ('last_name', 'first_name', 'speciality', 'city', 'cin')
    list_per_page = 10

admin.site.register(User, UserAdmin)