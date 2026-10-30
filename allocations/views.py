from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q, F
from rooms.models import Room
from accounts.models import User
from .models import Allocation
from .services import allocate_room, vacate_room


@login_required
def allocate_view(request):
    if not request.user.is_admin_role():
        messages.error(request, 'Only admins can allocate rooms.')
        return redirect('dashboards:home')

    if request.method == 'POST':
        student_roll = request.POST.get('student_roll')
        room_id = request.POST.get('room')

        try:
            # Look up student by Roll No (case insensitive)
            student = User.objects.get(roll_no__iexact=student_roll.strip(), role='student')
            room = Room.objects.get(pk=room_id)

            allocate_room(student, room)
            messages.success(request, f'Room {room.room_no} allocated to {student.username} (Roll: {student.roll_no}).')
            return redirect('allocations:list')

        except User.DoesNotExist:
            messages.error(request, f'No student found with Roll No: {student_roll}')
        except Room.DoesNotExist:
            messages.error(request, 'Invalid room selected.')
        except ValidationError as e:
            messages.error(request, e.message if hasattr(e, 'message') else str(e))

    # --- FILTERING LOGIC FOR ROOMS ---
    room_type_filter = request.GET.get('room_type', '')
    # Only show rooms with space
    rooms = Room.objects.filter(occupied__lt=F('capacity'), status='available')

    if room_type_filter:
        rooms = rooms.filter(room_type=room_type_filter)

    context = {
        'rooms': rooms,
        'room_type_filter': room_type_filter,
        'room_types': Room.ROOM_TYPE_CHOICES,
    }
    return render(request, 'allocations/allocate.html', context)


@login_required
def allocation_list(request):
    if request.user.is_admin_role() or request.user.is_technician():
        allocations = Allocation.objects.select_related('student', 'room').all()
    else:
        allocations = Allocation.objects.select_related('room').filter(student=request.user)
    return render(request, 'allocations/allocation_list.html', {'allocations': allocations})


@login_required
def vacate_view(request, pk):
    if not request.user.is_admin_role():
        messages.error(request, 'Only admins can vacate.')
        return redirect('dashboards:home')
    allocation = get_object_or_404(Allocation, pk=pk)
    try:
        vacate_room(allocation)
        messages.success(request, 'Room vacated.')
    except ValidationError as e:
        messages.error(request, str(e))
    return redirect('allocations:list')