from django.conf import settings
from django.db import models
from rooms.models import Room

class Allocation(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('vacated', 'Vacated'),
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='allocations')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='allocations')
    allocated_at = models.DateTimeField(auto_now_add=True)
    vacated_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    class Meta:
        ordering = ['-allocated_at']

    def __str__(self):
        return f"{self.student.username} -> {self.room}"