from django.contrib import admin
from .models import Room

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('block', 'room_no', 'room_type', 'capacity', 'occupied', 'status')
    list_filter = ('block', 'room_type', 'status')
    search_fields = ('room_no', 'block')