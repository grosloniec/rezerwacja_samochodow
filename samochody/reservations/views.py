from django.forms import ValidationError
from typing import Any
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, DetailView

from reservations.forms import ConfirmReservationForm, ListViewFilterForm
from reservations.models import Samochod, Klient, Rezerwacja
# Create your views here.

def filter_choice_field(qs, field, field_value):
    if field_value != "None": # jesli opcja cargo zostala podana
        qs = qs.filter(**{field: field_value}) # stworzenie key value arguements from dict
    return qs

def filter_non_required_field(qs, field, field_value):
    if field_value is not None:
        qs = qs.filter(**{field: field_value})
    return qs

class SamochodListView(ListView):
    model = Samochod
    template_name = "samochody_list.html"
    context_object_name = "object_list"

    def get_queryset(self):
        qs = Samochod.objects.filter(reservations=None)
        return qs

    def get_context_data(self, **kwargs: Any) -> dict:
        context = super().get_context_data(**kwargs)
        context["form"] = ListViewFilterForm(self.request.GET or None)
        return context

    def post(self, request, *args, **kwargs):
        qs = self.get_queryset()
        filter_form = ListViewFilterForm(self.request.POST)
        if filter_form.is_valid():
            seats = filter_form.cleaned_data["seats"]
            gearbox = filter_form.cleaned_data["gearbox"]
            fuel_type = filter_form.cleaned_data["fuel_type"]
            active_cruise_control = filter_form.cleaned_data["active_cruise_control"]
            body_type = filter_form.cleaned_data["body_type"]
            luggage_capacity = filter_form.cleaned_data["luggage_capacity"]
            air_conditioning = filter_form.cleaned_data["air_conditioning"]
            segment = filter_form.cleaned_data["segment"]
            price_per_day = filter_form.cleaned_data["price_per_day"]

            qs = filter_non_required_field(qs, field="seats", field_value=seats)
            qs = filter_choice_field(qs, field="gearbox", field_value=gearbox)
            qs = filter_choice_field(qs, field="fuel_type", field_value=fuel_type)
            qs = filter_choice_field(qs, field="active_cruise_control", field_value=active_cruise_control)
            qs = filter_choice_field(qs, field="body_type", field_value=body_type)
            qs = filter_non_required_field(qs, field="luggage_capacity__gte", field_value=luggage_capacity)
            qs = filter_choice_field(qs, field="air_conditioning", field_value=air_conditioning)
            qs = filter_choice_field(qs, field="segment", field_value=segment)
            qs = filter_non_required_field(qs, field="price_per_day__lte", field_value=price_per_day)

        context = {self.context_object_name: qs, 'form': filter_form}
        return render(request, self.template_name, context)


class SamochodDetailView(DetailView):
    model = Samochod
    template_name = "samochod_detail.html"

def confirm_reservation(request, samochod_id):
    # REQUEST METHODS
    # GET
    # POST
    # PUT
    # DELETE
    message = ""
    if request.method == "POST":
        form = ConfirmReservationForm(request.POST)
        if form.is_valid():
            klient, created = Klient.objects.get_or_create(
                            mail=form.cleaned_data["mail"],
                            defaults={
                                "name": form.cleaned_data["name"],
                                "surname": form.cleaned_data["surname"],
                                "phone": form.cleaned_data["phone"],
                                "birthday": form.cleaned_data["birthday"],
                                "driving_license_since": form.cleaned_data["driving_license_since"],
                            }
                        )
            samochod = get_object_or_404(Samochod, id=samochod_id)
            if not samochod.reservations.exists():
                rezerwacja = Rezerwacja.objects.create(klient=klient, samochod=samochod)
                print(f"Stworzono rezerwacje {rezerwacja}")
                return redirect("samochody-list")
            else:
                form = ConfirmReservationForm()
                message = "Ten samochod jest juz zarezerwowany"

    else:
        form = ConfirmReservationForm()

    return render(request, "confirm_reservation.html", {"form": form, "samochod_id": samochod_id, "message": message})