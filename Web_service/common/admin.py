from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import UserInfo, UseService

# Register your models here.
admin.site.register(UseService)

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('user_id', 'gender', 'age', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('user_id', 'password')}),
        ('Personal info', {'fields': ('gender','age',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user_id', 'gender', 'password1', 'password2')}
         ),
    )
    search_fields = ('user_id',)
    ordering = ('user_id',)
    filter_horizontal = ()


# User, UserAdmin 을 등록
admin.site.register(UserInfo, UserAdmin)