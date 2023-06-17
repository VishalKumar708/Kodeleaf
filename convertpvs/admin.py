from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin


# Register your models here.

class AdminAddProfile(admin.ModelAdmin):

    list_display = ('profile_id','profile_name','in_file_path','out_file_path','archieve_path','created_date','created_by','updated_date','updated_by')
    list_filter = ("profile_name",)

    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.opts.verbose_name_plural = "Add Profile"

admin.site.register(Add_Profile, AdminAddProfile)


class AdminAudit_log(ExportActionMixin, admin.ModelAdmin):
    list_display = ("cpv_audit_id", "user_name", "in_file_name", "out_file_name", "converted_datetime", "status", "cpv_System_Name", "profile_name")
    list_per_page = 20
    list_filter = ("user_name", "status")
    #  to remove modify record permission
    def has_change_permission(self, request, obj=None):
        return False
    # to remove add_profile button
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    def __init__(self, model, admin_site):
        super().__init__(model, admin_site)
        self.opts.verbose_name_plural = "Audit Log"


admin.site.register(audit_log, AdminAudit_log)

