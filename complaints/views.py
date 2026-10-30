from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Complaint
from .forms import ComplaintForm, AssignForm
from .services import transition_status
from accounts.models import User


@login_required
def submit_complaint(request):
    if not request.user.is_student():
        messages.error(request, 'Only students can submit complaints.')
        return redirect('dashboards:home')
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            c = form.save(commit=False)
            c.student = request.user
            c.save()
            messages.success(request, 'Complaint submitted.')
            return redirect('complaints:track')
    else:
        form = ComplaintForm()
    return render(request, 'complaints/submit.html', {'form': form})


@login_required
def track_complaints(request):
    if request.user.is_student():
        complaints = Complaint.objects.filter(student=request.user)
    elif request.user.is_technician():
        complaints = Complaint.objects.filter(assigned_to=request.user)
    else:
        complaints = Complaint.objects.all()
    return render(request, 'complaints/track.html', {'complaints': complaints})


@login_required
def assign_complaint(request, pk):
    if not request.user.is_admin_role():
        messages.error(request, 'Only admins can assign complaints.')
        return redirect('dashboards:home')
    complaint = get_object_or_404(Complaint, pk=pk)
    if request.method == 'POST':
        form = AssignForm(request.POST, instance=complaint)
        if form.is_valid():
            c = form.save(commit=False)
            if complaint.status == 'pending' and c.assigned_to:
                c.status = 'assigned'
            c.save()
            messages.success(request, 'Complaint updated.')
            return redirect('complaints:track')
    else:
        form = AssignForm(instance=complaint)
        form.fields['assigned_to'].queryset = User.objects.filter(role='technician')
    return render(request, 'complaints/assign.html', {'form': form, 'complaint': complaint})


@login_required
def technician_update(request, pk):
    if not request.user.is_technician():
        messages.error(request, 'Technicians only.')
        return redirect('dashboards:home')
    complaint = get_object_or_404(Complaint, pk=pk, assigned_to=request.user)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        try:
            transition_status(complaint, new_status, technician=request.user)
            messages.success(request, f'Status updated to {new_status}.')
        except ValueError as e:
            messages.error(request, str(e))
    return redirect('complaints:track')