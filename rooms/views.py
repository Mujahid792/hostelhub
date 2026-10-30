from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Room
from .forms import RoomForm


@login_required
def room_list(request):
    rooms = Room.objects.all()

    # Get filter parameters from the URL
    block_filter = request.GET.get('block')
    type_filter = request.GET.get('room_type')

    # Apply filters if they exist
    if block_filter:
        rooms = rooms.filter(block__iexact=block_filter)
    if type_filter:
        rooms = rooms.filter(room_type=type_filter)

    # Get unique blocks for the dropdown menu
    all_blocks = Room.objects.values_list('block', flat=True).distinct().order_by('block')

    context = {
        'rooms': rooms,
        'all_blocks': all_blocks,
        'selected_block': block_filter,
        'selected_type': type_filter,
        'room_types': Room.ROOM_TYPE_CHOICES,
    }
    return render(request, 'rooms/room_list.html', context)


@login_required
def room_create(request):
    if not request.user.is_admin_role():
        messages.error(request, 'Only admins can manage rooms.')
        return redirect('dashboards:home')
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created.')
            return redirect('rooms:list')
    else:
        form = RoomForm()
    return render(request, 'rooms/room_form.html', {'form': form, 'title': 'Create Room'})


@login_required
def room_edit(request, pk):
    if not request.user.is_admin_role():
        messages.error(request, 'Only admins can manage rooms.')
        return redirect('dashboards:home')
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated.')
            return redirect('rooms:list')
    else:
        form = RoomForm(instance=room)
    return render(request, 'rooms/room_form.html', {'form': form, 'title': 'Edit Room'})


@login_required
def room_delete(request, pk):
    if not request.user.is_admin_role():
        messages.error(request, 'Only admins can manage rooms.')
        return redirect('dashboards:home')
    room = get_object_or_404(Room, pk=pk)
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted.')
        return redirect('rooms:list')
    return render(request, 'rooms/room_confirm_delete.html', {'room': room})