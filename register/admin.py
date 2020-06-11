from .models import User, Department, Section
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# Register your models here.
@admin.register(Department)
class AdminDepartment(admin.ModelAdmin):
    pass


@admin.register(Section)
class AdminSection(admin.ModelAdmin):
    pass


@admin.register(User)
class AdminUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'email')}),
        (_('Personal info'), {'fields': ('department', 'section', 'level', 'union_class')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
    list_display = ('username', 'level', 'get_belongs', 'last_login', 'union_class')
    search_fields = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions')
