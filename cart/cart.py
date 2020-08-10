from decimal import Decimal
from django.conf import settings
from theater.models import *


class Cart(object):
    def __init__(self, request):
        """ Инициализируем корзину """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, ticket):
        """ Добавить продукт в корзину или обновить его количество. """
        ticket_id = str(ticket.id)
        if ticket_id not in self.cart:
            self.cart[ticket_id] = {'price': str(ticket.price)}
        self.save()

    def save(self):
        # Обновление сессии cart
        self.session[settings.CART_SESSION_ID] = self.cart
        # Отметить сеанс как "измененный", чтобы убедиться, что он сохранен
        self.session.modified = True

    def remove(self, ticket):
        """ Удаление товара из корзины. """
        ticket_id = str(ticket.id)
        if ticket_id in self.cart:
            del self.cart[ticket_id]
            self.save()

    def __iter__(self):
        """ Перебор элементов в корзине и получение продуктов из базы данных. """
        ticket_ids = self.cart.keys()
        # получение объектов product и добавление их в корзину
        tickets = Ticket.objects.filter(id__in=ticket_ids)
        for ticket in tickets:
            self.cart[str(ticket.id)]['ticket'] = ticket

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price']
            yield item

    def get_total_price(self):
        """ Подсчет стоимости товаров в корзине. """
        return sum(Decimal(item['price']) for item in self.cart.values())

    def clear(self):
        # удаление корзины из сессии
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
