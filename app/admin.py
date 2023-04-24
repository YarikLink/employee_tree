from django.contrib import admin
from app.models import Employee



@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['name', 'position', 'manager_name']

    def manager_name(self, obj):
        return obj.manager