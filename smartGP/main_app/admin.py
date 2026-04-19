from django.contrib import admin
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'mobile_number', 'is_staff', 'is_superuser')
    search_fields = ('username', 'email', 'mobile_number')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Complaint)
admin.site.register(SchemeApplication)
admin.site.register(News)

# Register your models here.
