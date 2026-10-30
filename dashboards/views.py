from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from rooms.models import Room
from allocations.models import Allocation
from complaints.models import Complaint
from gatepass.models import GatePass
from accounts.models import User


@login_required
def home(request):
    if request.user.is_admin_role():
        return redirect('dashboards:admin')
    if request.user.is_technician():
        return redirect('dashboards:technician')
    return redirect('dashboards:student')


@login_required
def student_dashboard(request):
    if not request.user.is_student():
        return redirect('dashboards:home')
    allocation = Allocation.objects.filter(student=request.user, status='active').select_related('room').first()
    complaints = Complaint.objects.filter(student=request.user)[:5]
    passes = GatePass.objects.filter(student=request.user)[:5]
    context = {
        'allocation': allocation,
        'complaints': complaints,
        'passes': passes,
    }
    return render(request, 'dashboards/student.html', context)


@login_required
def admin_dashboard(request):
    if not request.user.is_admin_role():
        return redirect('dashboards:home')
    total_rooms = Room.objects.count()
    total_capacity = sum(r.capacity for r in Room.objects.all())
    total_occupied = sum(r.occupied for r in Room.objects.all())
    stats = {
        'total_rooms': total_rooms,
        'total_capacity': total_capacity,
        'total_occupied': total_occupied,
        'total_students': User.objects.filter(role='student').count(),
        'pending_complaints': Complaint.objects.filter(status='pending').count(),
        'pending_gatepasses': GatePass.objects.filter(status='pending').count(),
    }
    recent_complaints = Complaint.objects.all()[:5]
    recent_allocations = Allocation.objects.select_related('student', 'room').all()[:5]
    return render(request, 'dashboards/admin.html', {
        'stats': stats,
        'recent_complaints': recent_complaints,
        'recent_allocations': recent_allocations,
    })


@login_required
def technician_dashboard(request):
    if not request.user.is_technician():
        return redirect('dashboards:home')
    assigned = Complaint.objects.filter(assigned_to=request.user)
    stats = {
        'assigned': assigned.count(),
        'in_progress': assigned.filter(status='in_progress').count(),
        'resolved': assigned.filter(status='resolved').count(),
    }
    return render(request, 'dashboards/technician.html', {'stats': stats, 'complaints': assigned})