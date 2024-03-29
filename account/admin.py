from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .forms import *
from .models import *


# Register your models here.


class UserAdministrator(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'is_admin', 'has_migrated_pwd', 'first_name', 'last_name')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'has_migrated_pwd', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('data_transfer_permission',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'has_migrated_pwd', 'first_name', 'last_name', 'data_transfer_permission',)}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


@admin.register(IAM)
class IAMAdmin(admin.ModelAdmin):
    list_display = ('user', 'aws_user', 'aws_access_key', 'created_on')


@admin.register(AWSRequest)
class AWSAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'created_on')


@admin.register(AnaGroup)
class AWSAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_on')


admin.site.register(User, UserAdministrator)
admin.site.unregister(Group)
# admin.site.register(IAM)
# admin.site.register(AWSRequest)
