from django.db import models

class Room(models.Model):
    ROOM_TYPE_CHOICES = (
        ('single', 'Single'),
        ('double', 'Double'),
        ('triple', 'Triple'),
        ('quad', 'Quad'),
    )
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('full', 'Full'),
        ('maintenance', 'Maintenance'),
    )
    block = models.CharField(max_length=20)
    room_no = models.CharField(max_length=20, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES, default='double')
    capacity = models.PositiveIntegerField(default=2)
    occupied = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    class Meta:
        ordering = ['block', 'room_no']

    def available_space(self):
        return max(self.capacity - self.occupied, 0)

    def is_full(self):
        return self.occupied >= self.capacity

    def update_status(self):
        if self.status == 'maintenance':
            return
        self.status = 'full' if self.is_full() else 'available'
        self.save(update_fields=['status'])

    def __str__(self):
        return f"{self.block}-{self.room_no} ({self.room_type})"