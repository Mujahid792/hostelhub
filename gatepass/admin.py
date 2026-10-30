from django.contrib import admin
from .models import GatePass

@admin.register(GatePass)
class GatePassAdmin(admin.ModelAdmin):
    list_display = ('id', 'student', 'destination', 'departure_date', 'return_date', 'status')
    list_filter = ('status',)