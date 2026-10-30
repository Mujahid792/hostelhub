from django.contrib import admin
from .models import SMSLog

@admin.register(SMSLog)
class SMSLogAdmin(admin.ModelAdmin):
    list_display = ('to_number', 'status', 'created_at')
    list_filter = ('status',)