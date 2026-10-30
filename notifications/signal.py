from django.db.models.signals import post_save
from django.dispatch import receiver
from allocations.models import Allocation
from gatepass.models import GatePass
from .services import send_sms


@receiver(post_save, sender=Allocation)
def notify_allocation(sender, instance, created, **kwargs):
    if created and instance.student.phone:
        send_sms(
            to=instance.student.phone,
            body=f"HostelHub: You have been allocated room {instance.room.room_no} in block {instance.room.block}."
        )


@receiver(post_save, sender=GatePass)
def notify_gatepass(sender, instance, created, **kwargs):
    if not created and instance.status in ('approved', 'rejected') and instance.student.phone:
        send_sms(
            to=instance.student.phone,
            body=f"HostelHub: Your gate pass #{instance.pk} has been {instance.status}."
        )