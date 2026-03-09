from .models import AuditLog

def log_action(user, visitor, action, description=None):

    AuditLog.objects.create(
        user=user,
        visitor=visitor,
        action=action,
        description=description
    )