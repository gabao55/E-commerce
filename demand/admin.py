from django.contrib import admin
from . import models

class DemandItemInline(admin.TabularInline):
    model = models.DemandItem
    extra = 1

class DemandAdmin(admin.ModelAdmin):
    inlines = [
        DemandItemInline
    ]

# Register your models here.
admin.site.register(models.Demand, DemandAdmin)
admin.site.register(models.DemandItem)