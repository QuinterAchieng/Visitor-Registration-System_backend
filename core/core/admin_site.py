from django.contrib.admin import AdminSite
from django.utils import timezone
from visitors.models import Visitor

class CustomAdminSite(AdminSite):
    site_header = "Visitor Management Dashboard"
    site_title = "Visitor System"
    index_title = "Overview"

    def each_context(self, request):
        context = super().each_context(request)

        today = timezone.now().date()

        context['today_visitors'] = Visitor.objects.filter(
            check_in_time__date=today
        ).count()

        context['current_visitors'] = Visitor.objects.filter(
            checked_out=False
        ).count()

        context['total_visitors'] = Visitor.objects.count()

        return context
