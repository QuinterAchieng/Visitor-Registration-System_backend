from django.contrib import admin
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from visitors.models import Visitor, AuditLog
from visitors.admin import VisitorAdmin, AuditLogAdmin


class CustomAdminSite(admin.AdminSite):
    site_header = "Visitor Management Dashboard"

    def index(self, request, extra_context=None):
        today = timezone.now().date()

        # =========================
        # Analytics Numbers
        # =========================
        total_visitors = Visitor.objects.count()

        todays_visitors = Visitor.objects.filter(
            check_in_time__date=today
        ).count()

        current_visitors = Visitor.objects.filter(
            checked_out=False
        ).count()

        # =========================
        # Detailed Lists
        # =========================
        today_visitors_list = Visitor.objects.filter(
            check_in_time__date=today
        ).select_related("department", "purpose")

        current_visitors_list = Visitor.objects.filter(
            checked_out=False
        ).select_related("department", "purpose")

        # =========================
        # Send to Template
        # =========================
        extra_context = extra_context or {}
        extra_context.update({
            "total_visitors": total_visitors,
            "todays_visitors": todays_visitors,
            "current_visitors": current_visitors,
            "today_visitors_list": today_visitors_list,
            "current_visitors_list": current_visitors_list,
        })

        return super().index(request, extra_context)


# =========================
# Create Custom Admin Site
# =========================
custom_admin_site = CustomAdminSite(name="custom_admin")

User = get_user_model()

# =========================
# Register Models
# =========================
custom_admin_site.register(User, UserAdmin)
custom_admin_site.register(Group, GroupAdmin)
custom_admin_site.register(AuditLog, AuditLogAdmin)