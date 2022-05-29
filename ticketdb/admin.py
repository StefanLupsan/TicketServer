from django.contrib import admin
from .models import AfterTicket
from .models import PromTicket

# Register your models here.


class PromTicketAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name', 'email', 'is_valid', 'age', 'mail_sent']


class AfterTicketAdmin(admin.ModelAdmin):
    ordering = ['name']
    search_fields = ['name', 'email', 'is_valid', 'age', 'mail_sent']


admin.site.register(AfterTicket, AfterTicketAdmin)
admin.site.register(PromTicket, PromTicketAdmin)
