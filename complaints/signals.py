from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Complaint

@receiver(post_save, sender=Complaint)
def notify_status_change(sender, instance, created, **kwargs):
    if created:
        return
    # Delegate to notifications app (lazy import to avoid circular)
    try:
        from notifications.services import send_sms
        if instance.student.phone:
            send_sms(
                to=instance.student.phone,
                body=f"HostelHub: Complaint #{instance.pk} status is now {instance.get_status_display()}."
            )
    except Exception:
        pass