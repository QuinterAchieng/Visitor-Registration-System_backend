from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Visitor, AuditLog

User = get_user_model()





# CREATE + UPDATE AUDIT LOGGING


@receiver(post_save, sender=Visitor)
def visitor_save_audit(sender, instance, created, **kwargs):

    action = "CREATE" if created else "UPDATE"

    AuditLog.objects.create(
        user=instance.recorded_by,   # ✅ Use model stored user
        action=action,
        visitor=instance,
        description=f"Visitor {instance.full_name} {action.lower()}d"
    )




# DELETE AUDIT LOGGING


@receiver(post_delete, sender=Visitor)
def visitor_delete_audit(sender, instance, **kwargs):

    AuditLog.objects.create(
        user=instance.recorded_by,   # ✅ Use stored creator
        action="DELETE",
        visitor=instance,
        description=f"Visitor {instance.full_name} deleted"
    )
    