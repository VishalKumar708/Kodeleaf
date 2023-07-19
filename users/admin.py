from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.http import HttpResponseRedirect

from import_export.admin import ExportActionMixin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

# to remove or hide extra permissions from admin dashboard
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
# to change text from password
from django.contrib.auth.forms import AdminPasswordChangeForm


class CustomUserAdmin(ExportActionMixin,UserAdmin):
    readonly_fields = ('date_joined',)
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email","first_name","last_name", "is_staff", "is_active","date_joined")
    list_filter = ("email", "is_staff", "is_active",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")+readonly_fields}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "first_name", "last_name", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)
    change_password_form = AdminPasswordChangeForm #helpful

    # def get_form(self, request, obj=None, **kwargs):
    #     form = super().get_form(request, obj, **kwargs)
    #     # form.declared_fields['password'].help_text = format_html(
    #     #     '<a href="{}">Reset Password</a>.',
    #     #     reverse('admin:auth_user_password_change', args=[obj.id]) if obj else ''
    #     # )
    #     return form
    # ________________________________________________________

    # ____________________________________________________
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "user_permissions":

            # Exclude specific permissions from the form field
            excluded_permissions = [
                ('auth', 'permission'),  # Exclude 'auth | permission'
                ('sessions', 'session'),  # Exclude 'sessions | session'
                ('contenttypes', 'contenttype'),
                ('auth', 'group'), # Exclude 'contenttypes | contenttype'
                ('admin', 'logentry'),
                ('django_celery_beat', 'clockedschedule'),
                ('django_celery_beat', 'solarschedule'),
                ('django_celery_results', 'groupresult'),
                ('django_celery_results','chordcounter'),
                ('django_celery_beat','crontabschedule')
            ]

            kwargs["queryset"] = Permission.objects.exclude(
                content_type__in=[ContentType.objects.get(app_label=app_label, model=model) for app_label, model in excluded_permissions]
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def has_delete_permission(self, request, obj=None):
        return False




admin.site.register(CustomUser, CustomUserAdmin)

from django.contrib.auth.admin import GroupAdmin
from django.contrib.auth.models import Group #,Permission
from .models import CustomGroup

# from django.contrib.contenttypes.models import ContentType


class CustomGroupAdmin(GroupAdmin):


    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == "permissions":


            # Exclude specific permissions from the form field
            excluded_permissions = [
                ('auth', 'permission'),  # Exclude 'auth | permission'
                ('sessions', 'session'),  # Exclude 'sessions | session'
                ('contenttypes', 'contenttype'),
                ('auth', 'group'),  # Exclude 'contenttypes | contenttype'
                ('admin', 'logentry'),
                ('django_celery_beat', 'clockedschedule'),
                ('django_celery_beat', 'solarschedule'),
                ('django_celery_results', 'groupresult'),
                ('django_celery_results', 'chordcounter'),
                ('django_celery_beat', 'crontabschedule')
            ]

            kwargs["queryset"] = Permission.objects.exclude(
                content_type__in=[ContentType.objects.get(app_label=app_label, model=model) for app_label, model in excluded_permissions]
            )

        return super().formfield_for_manytomany(db_field, request, **kwargs)


    # def get_deleted_objects(self, objs, request):
    #     return super().get_deleted_objects(objs,request)



admin.site.unregister(Group)
admin.site.register(CustomGroup, CustomGroupAdmin)






