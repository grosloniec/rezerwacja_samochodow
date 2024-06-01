from django import forms

from reservations.models import Samochod, SamochodBodyType

def create_choices(choice_list):
    li = [("None", "------"),]
    li2 = [choice for choice in choice_list]
    li.extend(li2)
    return li

class ConfirmReservationForm(forms.Form):
    name = forms.CharField(max_length=32)
    surname = forms.CharField(max_length=32)
    mail = forms.EmailField()
    phone = forms.CharField(max_length=16)
    birthday = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    driving_license_since = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

class ListViewFilterForm(forms.Form):
    seats = forms.IntegerField(min_value=1, required=False)
    gearbox = forms.ChoiceField(choices=create_choices(Samochod.SAMOCHOD_GEARBOX_CHOICES), required=False)
    fuel_type = forms.ChoiceField(choices=create_choices(Samochod.SAMOCHOD_FUEL_TYPE_CHOICES), required=False)
    active_cruise_control = forms.ChoiceField(choices=[("None", "------"),(True, "TRUE"), (False, "FALSE"),], required=False)
    body_type = forms.ChoiceField(choices=create_choices(SamochodBodyType.choices()), required=False)
    luggage_capacity = forms.DecimalField(decimal_places=0, max_digits=4, required=False, label="Min luggage capacity")
    air_conditioning = forms.ChoiceField(choices=create_choices(Samochod.SAMOCHOD_AIR_CONDITIONING_CHOICES), required=False)
    segment = forms.ChoiceField(choices=create_choices(Samochod.SAMOCHOD_SEGMENT_CHOICES), required=False)
    price_per_day = forms.DecimalField(decimal_places=2, max_digits=6, required=False, label="Max price per day")