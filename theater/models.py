from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.


class Performance(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    image = models.ImageField(null=True, blank=True, upload_to='performance/')
    title = models.CharField(max_length=50, null=False, db_index=True)
    description = models.TextField(null=True)
    date = models.DateField(null=False, db_index=True)
    time = models.TimeField(null=False,db_index=True)

    class Meta:
        db_table = 'theater_performance'
        ordering = ('date',)
        index_together = [
            ['title'],
            ['date'],
            ['date', 'time']
        ]

    def __str__(self):
        return f"{self.title} - {self.date}, {self.time}"


class Sector(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    name = models.CharField(max_length=30, null=False, db_index=True, unique=True)

    class Meta:
        index_together = [
            ['name']
        ]

    def __str__(self):
        return f"{self.name}"


class Row(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    number = models.PositiveIntegerField(null=False, db_index=True, unique=True)

    def __str__(self):
        return f"Ряд №{self.number}"


class Seat(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    number = models.PositiveIntegerField(null=False, db_index=True, unique=True)

    def __str__(self):
        return f"Место №{self.number}"


class Price(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    price = models.DecimalField(null=False, max_digits=5, decimal_places=2, unique=True, default=0)

    def __str__(self):
        return f"{self.price}"


class Ticket(models.Model):
    id = models.AutoField(auto_created=True, primary_key=True)
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    sector = models.ForeignKey(Sector, on_delete=models.PROTECT)
    row = models.ForeignKey(Row, on_delete=models.PROTECT)
    seat = models.ForeignKey(Seat, on_delete=models.PROTECT)
    price = models.ForeignKey(Price, on_delete=models.PROTECT)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = [['performance', 'sector', 'row', 'seat']]

    def __str__(self):
        return f"{self.id}: {self.performance.title}, сектор {self.sector.name}, ряд №{self.row.number}, " \
               f"место №{self.seat.number}"

