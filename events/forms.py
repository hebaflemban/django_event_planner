from django import forms
from django.contrib.auth.models import User
from .models import Event, Tag, Reservation
from django.core.exceptions import ValidationError


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


class UserProfile(forms.ModelForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name']


class ReservationForm(forms.ModelForm):
	class Meta:
		model = Reservation
		fields = ['num_tickets']


class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		exclude = ['created_by', 'slug']
		widgets = { 'tags': forms.CheckboxSelectMultiple ,
					'date': forms.DateInput(attrs={'type': 'date-local'}),
					'time': forms.TimeInput(attrs={'type': 'time'})
					}


class TagForm(forms.Form):
	class Meta:
		model = Tag
		fields = '__all__'
