from django.utils import timezone
from .models import Complaint

VALID_TRANSITIONS = {
    'pending': ['assigned', 'rejected'],
    'assigned': ['in_progress', 'rejected'],
    'in_progress': ['resolved', 'rejected'],
    'resolved': [],
    'rejected': [],
}


def transition_status(complaint, new_status, technician=None):
    if new_status not in VALID_TRANSITIONS.get(complaint.status, []):
        raise ValueError(f'Invalid transition {complaint.status} -> {new_status}')
    complaint.status = new_status
    if new_status == 'assigned' and technician:
        complaint.assigned_to = technician
    complaint.save()
    return complaint


def upload_image(complaint, uploaded_file):
    if not uploaded_file:
        return complaint
    complaint.image = uploaded_file
    complaint.save(update_fields=['image'])
    return complaint