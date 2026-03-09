from django.contrib import admin
from django.http import HttpResponse
from .models import Ticket
import csv

class TicketAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'created_at')
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename=tickets.csv'

        writer = csv.writer(response)
        writer.writerow(['Name', 'Email', 'Service', 'Description', 'Created At'])

        for ticket in queryset:
            writer.writerow([ticket.name, ticket.email, ticket.service, ticket.description, ticket.created_at])

        return response

    export_as_csv.short_description = "Export Selected Tickets as CSV"

admin.site.register(Ticket, TicketAdmin)



