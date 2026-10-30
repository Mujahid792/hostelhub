from django.contrib import admin
from .models import Complaint

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'student', 'category', 'status', 'priority', 'assigned_to', 'created_at')
    list_filter = ('status', 'category', 'priority')
    search_fields = ('title', 'description')