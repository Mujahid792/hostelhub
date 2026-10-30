from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import GatePass
from .forms import GatePassForm


@login_required
def request_pass(request):
    if not request.user.is_student():
        messages.error(request, 'Only students can request gate passes.')
        return redirect('dashboards:home')
    if request.method == 'POST':
        form = GatePassForm(request.POST)
        if form.is_valid():
            gp = form.save(commit=False)
            gp.student = request.user
            gp.save()
            messages.success(request, 'Gate pass requested.')
            return redirect('gatepass:list')
    else:
        form = GatePassForm()
    return render(request, 'gatepass/request.html', {'form': form})


@login_required
def gatepass_list(request):
    if request.user.is_student():
        passes = GatePass.objects.filter(student=request.user)
    else:
        passes = GatePass.objects.all()
    return render(request, 'gatepass/list.html', {'passes': passes})


@login_required
def approve_pass(request, pk):
    if not request.user.is_admin_role():
        messages.error(request, 'Only admins can approve gate passes.')
        return redirect('dashboards:home')
    gp = get_object_or_404(GatePass, pk=pk)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            gp.status = 'approved'
            gp.approved_by = request.user
        elif action == 'reject':
            gp.status = 'rejected'
        gp.save()
        messages.success(request, f'Gate pass {gp.status}.')
        return redirect('gatepass:list')
    return render(request, 'gatepass/approve.html', {'gp': gp})