from django.contrib.auth.models import User
from theater.models import *
import datetime

# Create your models here.


class Status(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('in the execution', 'В исполнении'),
        ('completed', 'Завершен'),
        ('rejected', 'Отклонен'),
    ]
    FINISHED = {
        'Отклонен',
        'Завершен'
    }
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=20, null=False, db_index=True, choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.name}"


class Order(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=1, null=False)
    amount = models.PositiveIntegerField(default=1, null=False)
    create_date = models.DateTimeField(editable=False, null=True)

    class Meta:
        ordering = ('-id',)

    def __str__(self):
        return f"Заказ №{self.id} - {self.status}"

    def save(self, *args, **kwargs):
        self.create_date = datetime.datetime.now()
        if self.status.name == "Отклонен":
            for ticket in (ohs.ticket for ohs in self.items.all()):
                Ticket.objects.filter(id=ticket.id).update(available=True)
        super(Order, self).save(*args, **kwargs)


class OrderHasTicket(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    ticket = models.ForeignKey(Ticket, on_delete=models.PROTECT, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['order', 'ticket']


