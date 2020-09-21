from django import forms
from django.contrib.auth.models import User
from .models import Event, Tag, Reservation

class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


# class ReservationForm(forms.Form):
#     num_tickets = forms.IntegerField(min_value=1, max_value=5)


# class TicketForm(forms.Form):
#     class Meta:
#         model = Reservation
#         fields = ['num_tickets']
#
#
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['num_tickets']


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['created_by', 'attendees', 'slug', 'remaining_tickets']
        widgets = { 'tags': forms.CheckboxSelectMultiple ,
                    'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})}



class TagForm(forms.Form):
    class Meta:
        model = Tag
        fields = '__all__'
