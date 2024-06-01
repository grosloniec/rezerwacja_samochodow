from enum import Enum
from django.db import models
import datetime
from decimal import Decimal


# Create your models here.

class SamochodBodyType(Enum):
    SEDAN = "sedan"
    WAGON = "wagon"
    HATCHBACK = "hatchback"
    CONVERTIBLES = "convertibles"
    SUV = "SUV"
    VAN = "van"

    @classmethod
    def choices(cls):
        return [(i.name, i.value) for i in cls]


class Samochod(models.Model):
    SAMOCHOD_GEARBOX_CHOICES = [("AUTOMATIC", "automatic"), ("MANUAL", "manual")]
    SAMOCHOD_FUEL_TYPE_CHOICES = [("GASOLINE", "gasoline"), ("DIESEL", "diesel"), ("ELECTRIC", "electric")]
    SAMOCHOD_AIR_CONDITIONING_CHOICES = [("AUTOMATIC", "automatic"), ("MANUAL", "manual")]
    SAMOCHOD_SEGMENT_CHOICES = [("A", "A"), ("B", "B"), ("C", "C"), ("D", "D"), ("E", "E"), ("F", "F"), ("S", "S"),
                                ("M", "M"), ("J", "J")]

    make = models.CharField(max_length=255, default="")
    model = models.CharField(max_length=255, default="")
    seats = models.PositiveSmallIntegerField()
    gearbox = models.CharField(choices=SAMOCHOD_GEARBOX_CHOICES, max_length=16)
    fuel_type = models.CharField(choices=SAMOCHOD_FUEL_TYPE_CHOICES, max_length=16, default="GASOLINE")
    active_cruise_control = models.BooleanField(default=False)
    body_type = models.CharField(choices=SamochodBodyType.choices(), max_length=16)
    luggage_capacity = models.DecimalField(decimal_places=0, max_digits=4, default=0)  # od 0 do 9999
    air_conditioning = models.CharField(choices=SAMOCHOD_AIR_CONDITIONING_CHOICES, max_length=16, default="MANUAL")
    segment = models.CharField(choices=SAMOCHOD_SEGMENT_CHOICES, max_length=16, default="A")
    price_per_day = models.DecimalField(decimal_places=2, max_digits=6)  # od 000.00 do 9999.99

    def __str__(self):
        return f"{self.id}/{self.make}/{self.model}/{self.price_per_day}"

    class Meta:
        verbose_name = "Samochód"
        verbose_name_plural = "Samochody"


class Klient(models.Model):
    name = models.CharField(max_length=32, default="")
    surname = models.CharField(max_length=32, default="")
    mail = models.EmailField(unique=True)
    phone = models.CharField(max_length=16)
    birthday = models.DateField()
    driving_license_since = models.DateField(default=datetime.date.today)

    class Meta:
        verbose_name = "Klient"
        verbose_name_plural = "Klienci"

    def __str__(self):
        return f"{self.id}/{self.mail}"


class Rezerwacja(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    klient = models.ForeignKey(Klient, on_delete=models.CASCADE)
    samochod = models.ForeignKey(Samochod, on_delete=models.PROTECT, related_name="reservations")
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        verbose_name = "Rezerwacja"
        verbose_name_plural = "Rezerwacje"

    def save(self, *args, **kwargs):
        days = 1
        self.price = self.samochod.price_per_day * days
        super(Rezerwacja, self).save(*args, **kwargs)
