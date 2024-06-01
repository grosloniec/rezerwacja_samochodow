from django.contrib import admin
from reservations.models import Samochod, Klient, Rezerwacja

# Register your models here.

class SamochodAdmin(admin.ModelAdmin):
    fields = ["id", "make", "model", "seats", "gearbox", "fuel_type", "active_cruise_control", "body_type",
              "luggage_capacity", "air_conditioning", "segment", "price_per_day"]
    search_fields = ('make', 'model')
    list_display = ["id", "make", "model", "seats", "gearbox", "fuel_type", "active_cruise_control", "body_type",
                    "luggage_capacity", "air_conditioning", "segment", "price_per_day"]
    readonly_fields = ["id"]
class KlientAdmin(admin.ModelAdmin):
    fields = ["name", "surname", "mail", "phone", "birthday", "driving_license_since"]
    search_fields = ('name', 'surname')
    list_display = ["name", "surname", "mail", "phone", "birthday", "driving_license_since"]

class RezerwacjaAdmin(admin.ModelAdmin):
    fields = ["id", "date_created", "klient", "samochod", "price"]
    list_display = ["id", "date_created", "klient", "samochod", "price"]
    readonly_fields = ["id", "price", "date_created"]

admin.site.register(Samochod, SamochodAdmin)
admin.site.register(Klient, KlientAdmin)
admin.site.register(Rezerwacja, RezerwacjaAdmin)