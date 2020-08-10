from django.contrib import admin
from .models import *

# Register your models here.


class PerformanceAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date', 'time']
    list_filter = ['date', 'time']
    list_editable = ['date', 'time']


class TicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'performance', 'sector', 'row', 'seat', 'price', 'available']
    list_editable = ['price']


admin.site.register(Performance, PerformanceAdmin)
admin.site.register(Ticket, TicketAdmin)

admin.site.register(Price)
admin.site.register(Sector)
admin.site.register(Seat)
admin.site.register(Row)

