from django.http import Http404, HttpResponse
from django.shortcuts import render
from .models import *
from django.db.models.expressions import RawSQL
from django.contrib.auth.decorators import login_required
from django.db import connection
from orders.models import *
from django.db.models import Count
from django.db.models import Sum

# Create your views here.


def index(request):
    context = {
        "performances": Performance.objects.raw('select * from theater_performance')
    }
    return render(request, "theater/index.html", context)


def performance(request, performance_id):
    try:
        context = {
            "performance": Performance.objects.get(id=RawSQL("SELECT id FROM theater_performance WHERE id = %s",
                                                             [performance_id]))
        }
    except Performance.DoesNotExist:
        raise Http404("Performance does not exist.")
    return render(request, "theater/performance.html", context)


@login_required
def ticket_selection(request, performance_id):
    try:
        performance = Performance.objects.get(id=RawSQL("SELECT id FROM theater_performance WHERE id = %s",
                                          [performance_id]))
        available = True
        tickets = Ticket.objects.filter(available=RawSQL("SELECT available FROM theater_ticket WHERE available = %s",
                                                         [available]),
                                        performance_id=RawSQL("SELECT performance_id FROM theater_ticket WHERE performance_id = %s",
                                                              [performance_id])).all()
        sectors = {ticket.sector for ticket in tickets}
        rows = {ticket.row for ticket in tickets}
        seats = {ticket.seat for ticket in tickets}
    except Performance.DoesNotExist:
        return HttpResponse("К сожалению, билет, который вы выбрали, уже куплен. Пожалуйста, выберите другой.")
    context = {
        "performance": performance,
        "sectors": sectors,
        "rows": rows,
        "seats": seats
    }
    return render(request, "theater/ticket_selection_form.html", context)





