from django.contrib import admin
from django import forms
from .models import AuditLog

from .models import Visitor, Department, Purpose, AuditLog
import csv
from django.http import HttpResponse



# ==========================================
# ADMIN FORM VALIDATION (FOR DJANGO ADMIN)
# ==========================================

class VisitorAdminForm(forms.ModelForm):

    class Meta:
        model = Visitor
        fields = "__all__"

    def clean_contact(self):
        contact = self.cleaned_data.get("contact")

        if not contact:
            raise forms.ValidationError("Contact is required")

        if not contact.isdigit():
            raise forms.ValidationError("Contact must contain numbers only")

        if len(contact) != 10:
           raise forms.ValidationError("Contact must be exactly 10 digits")

        return contact

    def clean_id_number(self):
        id_number = self.cleaned_data.get("id_number")

        if not id_number:
            raise forms.ValidationError("ID number is required")

        if not id_number.isdigit():
            raise forms.ValidationError("ID number must contain digits only")

        if len(id_number) != 8:
           raise forms.ValidationError("ID number must be exactly 8 digits")

        return id_number
# ==========================================
# EXPORT CSV FUNCTION
# ==========================================

def export_visitors_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=visitors.csv'

    writer = csv.writer(response)

    writer.writerow([
        "Full Name",
        "ID Number",
        "Contact",
        "Visitor Type",
        "Department",
        "Purpose",
        "Check-in Time",
        "Check-out Time",
        "Checked Out"
    ])

    for visitor in queryset:
        writer.writerow([
            visitor.full_name,
            visitor.id_number,
            visitor.contact,
            visitor.visitor_type,
            visitor.department.name if visitor.department else "",
            visitor.purpose.name if visitor.purpose else "",
            visitor.check_in_time,
            visitor.check_out_time,
            visitor.checked_out
        ])

    return response


export_visitors_csv.short_description = "Export selected visitors to CSV"

# ADMIN REGISTRATION
@admin.register(Visitor)
class VisitorAdmin(admin.ModelAdmin):


    form = VisitorAdminForm

    list_display = (
        'full_name',
        'id_number',
        'department',
        'check_in_time',
        'checked_out'
    )
    list_filter = ('department', 'checked_out')
    search_fields = ('full_name', 'id_number')

    actions = [export_visitors_csv]

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(Purpose)
class PurposeAdmin(admin.ModelAdmin):
    search_fields = ['name']


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'action',
        'visitor',
        'timestamp',
        'description'
    )

    list_filter = (
        'action',
        'timestamp',
        'user'
    )

    search_fields = (
        'visitor__full_name',
        'user__username',
        'description'
    )

    ordering = ('-timestamp',)
    
from .models import AuditLog

if not hasattr(AuditLog, "__str__"):
    def auditlog_str(self):
        return f"{self.user} - {self.action}"

    AuditLog.__str__ = auditlog_str