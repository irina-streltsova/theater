from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.http import Http404
from theater.models import *
from .cart import Cart
from .forms import CartAddTicketForm
from django.contrib.auth.decorators import login_required
from django.db.models.expressions import RawSQL

# Create your views here.


@login_required
@require_POST
def cart_add(request, performance_id):
    cart = Cart(request)
    sector = request.POST.get("selectedSector")
    row = request.POST.get("selectedRow")
    seat = request.POST.get("selectedSeat")
    ticket = Ticket.objects.get(performance_id=RawSQL("SELECT id FROM theater_performance WHERE id = %s",
                                                      [performance_id]),
                                sector=RawSQL("select sector_id from theater_ticket where sector_id = %s",
                                              [sector]),
                                row=RawSQL("select row_id from theater_ticket where row_id = %s",
                                              [row]),
                                seat=RawSQL("select seat_id from theater_ticket where seat_id = %s",
                                           [seat]))
    form = CartAddTicketForm(request.POST)
    if ticket.available:
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(ticket=ticket)
    else:
        raise Http404("Ticket does not exist. Select another ")
    return redirect('cart_detail')


@login_required
def cart_remove(request, ticket_id):
    cart = Cart(request)
    ticket = Ticket.objects.get(id=RawSQL("select id from theater_ticket where id = %s", [ticket_id]))
    cart.remove(ticket)
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/shopping_bag.html', {'cart': cart})


