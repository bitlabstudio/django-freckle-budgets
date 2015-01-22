"""Admin classes for the freckle_budgets app."""
from django.contrib import admin

from . import models


class MonthAdmin(admin.ModelAdmin):
    list_display = ['year', 'month', 'employees', 'public_holidays']


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'freckle_project_id', 'color', 'is_investment']


class ProjectMonthAdmin(admin.ModelAdmin):
    list_display = ['month', 'project', 'budget', 'rate']
    list_filter = ['project', ]


class YearAdmin(admin.ModelAdmin):
    list_display = ['year', 'sick_leave_days', 'vacation_days']


admin.site.register(models.Month, MonthAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.ProjectMonth, ProjectMonthAdmin)
admin.site.register(models.Year, YearAdmin)
