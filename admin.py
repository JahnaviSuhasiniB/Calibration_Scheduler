from django.contrib import admin
from .models import Machine, Calibration

class MachineAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'location')  
    search_fields = ('name', 'type', 'location')

class CalibrationAdmin(admin.ModelAdmin):
    list_display = ('id', 'machine', 'date', 'status', 'assigned_user')
    list_filter = ('status', 'date')
    search_fields = ('machine__name', 'status', 'assigned_user__username')

admin.site.register(Machine, MachineAdmin)
admin.site.register(Calibration, CalibrationAdmin)
