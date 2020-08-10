from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from orders.models import *
from .forms import LoginForm, UserRegistrationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.expressions import RawSQL

# Create your views here.


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/authorization_form.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/registration_form.html', {'user_form': user_form})


def authorization(request):
    if not request.user.is_authenticated:
        return render(request, "account/authorization_form.html", {"message": None})
    context = {
        "user": request.user
    }
    return render(request, "theater/index.html", context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], email=cd['email'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    usera = User.objects.get(username=cd['username'], email=cd['email'])
                    if usera.is_superuser:
                        login(request, user)
                        return HttpResponseRedirect(reverse("admin_page"))
                    else:
                        login(request, user)
                        return HttpResponseRedirect(reverse("index"))
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse("Your username and password didn't match. Please try again.")
    else:
        form = LoginForm()
    return render(request, 'account/authorization_form.html', {'form': form})


def user_logout(request):
    logout(request)
    return render(request, "account/authorization_form.html")


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})


@login_required
def admin_page(request):
    return redirect('admin_orders', status_id=1)


@login_required
def admin_orders(request, status_id):
    orders = Order.objects.filter(status_id=RawSQL("select status_id from orders_order where status_id = %s",
                                                   [status_id])).all()
    orderht = OrderHasTicket.objects.filter(order__in=orders).all()
    tickets = {order.ticket for order in orderht}
    performances = {ticket.performance for ticket in tickets}
    sectors = {ticket.sector for ticket in tickets}
    rows = {ticket.row for ticket in tickets}
    seats = {ticket.seat for ticket in tickets}
    context = {
        "orders": orders,
        "orderht": orderht,
        'tickets': tickets,
        'performances': performances,
        'sectors': sectors,
        'rows': rows,
        'seats': seats,
        "status_id": status_id,
        "status": Status.objects.get(id=RawSQL("select id from orders_status where id = %s", [status_id])),
        "statuses": Status.objects.all()
    }
    return render(request, 'admin/orders.html', context)


@login_required
def order_execute(request, order_id):
    Order.objects.filter(id=RawSQL('select id from orders_order where id = %s',
                                [order_id])).update(status_id=2)
    order = Order.objects.get(id=RawSQL('select id from orders_order where id = %s',
                                [order_id]))
    order.save()
    return redirect('admin_orders', status_id=1)


@login_required
def order_complete(request, order_id):
    Order.objects.filter(id=RawSQL('select id from orders_order where id = %s',
                                [order_id])).update(status_id=3)
    order = Order.objects.get(id=RawSQL('select id from orders_order where id = %s',
                                        [order_id]))
    order.save()
    return redirect('admin_orders', status_id=2)


@login_required
def order_reject(request, order_id):
    Order.objects.filter(id=RawSQL('select id from orders_order where id = %s',
                                [order_id])).update(status_id=4)
    order = Order.objects.get(id=RawSQL('select id from orders_order where id = %s',
                                        [order_id]))
    order.save()
    return redirect('admin_orders', status_id=2)