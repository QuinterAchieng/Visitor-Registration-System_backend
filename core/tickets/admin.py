from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('title', 'description')

