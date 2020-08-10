from django.contrib import admin
from .models import *

# Register your models here.


class OHTInLine(admin.TabularInline):
    model = OrderHasTicket
    extra = 2


class OrderAdmin(admin.ModelAdmin):
    inlines = (OHTInLine, )
    list_display = ['id', 'user', 'status', 'amount', 'create_date', 'total_price']
    list_filter = ['status', 'total_price']
    list_editable = ['status']


admin.site.register(Order, OrderAdmin)
admin.site.register(Status)

# Register your models here.
