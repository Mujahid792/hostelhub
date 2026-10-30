from django.db import transaction
from django.core.exceptions import ValidationError
from rooms.models import Room
from .models import Allocation


@transaction.atomic
def allocate_room(student, room):
    # Lock row to prevent race conditions
    room = Room.objects.select_for_update().get(pk=room.pk)

    if room.status == 'maintenance':
        raise ValidationError('Room is under maintenance.')

    if room.is_full():
        raise ValidationError('Room is full. Overbooking prevented.')

    if Allocation.objects.filter(student=student, status='active').exists():
        raise ValidationError('Student already has an active allocation.')

    allocation = Allocation.objects.create(student=student, room=room)
    room.occupied += 1
    room.save(update_fields=['occupied'])
    room.update_status()
    return allocation


@transaction.atomic
def vacate_room(allocation):
    if allocation.status != 'active':
        raise ValidationError('Allocation is not active.')
    room = Room.objects.select_for_update().get(pk=allocation.room.pk)
    allocation.status = 'vacated'
    from django.utils import timezone
    allocation.vacated_at = timezone.now()
    allocation.save(update_fields=['status', 'vacated_at'])
    room.occupied = max(room.occupied - 1, 0)
    room.save(update_fields=['occupied'])
    room.update_status()
    return allocation