from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import LabLog, Role, LabMembership


@receiver(post_save, sender=LabMembership)
def log_membership_activity(sender, instance, created, **kwargs):
    """
    Log lab membership creation and role changes for admin review
    """
    if created:
        # Log when a new member joins the lab
        LabLog.objects.create(
            lab=instance.lab,
            user=instance.user,
            action="Member joined",
            details=f"User '{instance.user.username}' joined lab '{instance.lab.name}' with role '{instance.role.name}'"
        )
    else:
        # Log when a member's role is changed
        LabLog.objects.create(
            lab=instance.lab,
            user=instance.user,
            action="Role changed",
            details=f"User '{instance.user.username}' role changed to '{instance.role.name}' in lab '{instance.lab.name}'"
        )


@receiver(post_delete, sender=LabMembership)
def log_membership_removal(sender, instance, **kwargs):
    """
    Log when a member is removed from the lab
    """
    LabLog.objects.create(
        lab=instance.lab,
        user=instance.user,
        action="Member removed",
        details=f"User '{instance.user.username}' was removed from lab '{instance.lab.name}' (previous role: {instance.role.name})"
    )


