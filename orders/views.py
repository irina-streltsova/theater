from django.shortcuts import render, redirect
from orders.models import *
from cart.cart import Cart
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def order_create(request):
    cart = Cart(request)
    if cart.get_total_price() == 0:
        return render(request, "cart/shopping_bag.html")
    order = Order.objects.create(user=request.user, total_price=cart.get_total_price())
    order.save()
    ticket_amount = 0
    for item in cart:
        orderht = OrderHasTicket.objects.create(order=order, ticket=item['ticket'], price=item['price'])
        orderht.save()
        ticket = item['ticket']
        Ticket.objects.filter(id=ticket.id).update(available=False)
        ticket_amount += 1
    # очистка корзины
    cart.clear()
    Order.objects.filter(id=order.id).update(amount=ticket_amount)
    return redirect('my_orders')


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).all()
    orderhts = OrderHasTicket.objects.filter(order__in=orders).all()
    tickets = {order.ticket for order in orderhts}
    performances = {ticket.performance for ticket in tickets}
    sectors = {ticket.sector for ticket in tickets}
    rows = {ticket.row for ticket in tickets}
    seats = {ticket.seat for ticket in tickets}
    context = {
        'orders': orders,
        'orderhts': orderhts,
        'tickets': tickets,
        'performances': performances,
        'sectors': sectors,
        'rows': rows,
        'seats': seats
    }
    return render(request, "orders/created.html", context)


