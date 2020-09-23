from django.shortcuts import render, redirect
from django.contrib import admin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.db.models.signals import pre_save
from django.db.models import Q
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from django.http import Http404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import UserSignup, UserLogin, UserProfile, EventForm, ReservationForm
from .models import Event, Connection, Tag, Reservation



def dashboard(request, user_id):
    can_follow = True
    user = User.objects.get(id = user_id)

    if user.followers.filter(following_user=request.user).exists():
        can_follow = False

    if 'follow-unfollow' in request.POST:
        if user.followers.filter(user = user, following_user=request.user).exists():
            user.followers.filter(user = user, following_user=request.user).delete()
        else:
            new_connection = Connection(user = user , following_user = request.user )
            new_connection.save()

    context = {
        'can_follow' : can_follow,
        'profile' : user,
        "upcoming_resevations" : user.reservations.filter(event_date__gte = timezone.now()),
        "past_reservations" : user.reservations.filter(event_date__lt = timezone.now())
    }
    return render (request, 'dashboard.html', context)


def home(request):
    return render(request, 'home.html')


def update_profile(request, user_id):
    if not request.user.is_authenticated:
        messages.warning(request, "messages : You don\'t have access ")
        raise Http404('You don\'t have access ')
    form = UserProfile(instance=request.user)
    if request.method == "POST":
        form = UserProfile(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard', request.user.id)
    context = {
        'form': form,
    }
    return render (request, 'update_profile.html', context)


def events_list(request):
    active_events = Event.objects.all()
    # filter(date__gte = timezone.now())
    search_result = None
    search_term = None
    if 'search_events' in request.GET:
        search_term = request.GET['search_events']
        search_result = active_events.filter(Q(name__icontains=search_term) |
                        Q(description__icontains=search_term) | Q(created_by__username__icontains=search_term))
    context = {
        'events': active_events,
        'search_result' : search_result
    }
    return render(request, 'events_list.html', context)


def event_details(request, event_slug):
    event = Event.objects.get(slug = event_slug)
    context = {
        "event" : event,
    }
    return render(request, 'event_details.html', context)


def reservation_details(request, reservation_id):
    reservation = Reservation.objects.get(id = reservation_id)
    can_cancel = True

    if (reservation.event_date == datetime.now().date()) \
        and (reservation.event_time.hour-datetime.now().time().hour < 3):
        can_cancel = False

    if 'cancel_reservation' in request.POST:
        if can_cancel:
            reservation.delete()

    context = {
        "reservation" : reservation,
        "can_cancel" : can_cancel
    }
    return render(request, 'reservation_details.html', context)

# def cancel_reservation(request, reservation_id):
#     return can_cancel (request, 'dashboard.html', context)
#




def create_event(request):
    if not request.user.is_authenticated:
        messages.warning(request, "messages : You don\'t have access ")
        raise Http404('You don\'t have access ')
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = request.user
            event.max_capacity = form.cleaned_data['max_capacity']
            event.remaining_tickets = event.max_capacity
            event.save()

            return redirect('events_list')
    context = {
        'form': form,
    }
    return render(request, 'create_event.html', context)


def update_event(request, event_slug):
    event = Event.objects.get(slug=event_slug)
    if request.user != event.created_by:
        messages.warning(request, "messages : You don\'t have access ")
        raise Http404('You don\'t have access ')
    form = EventForm(instance=event)
    if request.method == "POST":
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('events_list')
    context = {
        'form': form,
        'event': event,
    }
    return render(request, 'update_event.html', context)


def book_tickets(request, event_slug):
    if not request.user.is_authenticated:
        messages.warning(request, "messages : You don\'t have access ")
        raise Http404('You don\'t have access ')
    event = Event.objects.get(slug=event_slug)
    form = ReservationForm()
    if request.method == "POST":
        form = ReservationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['num_tickets'] > event.remaining_tickets:
                messages.warning(request, f"Sorry there is only {event.remaining_tickets} tickets left for this event")
                return redirect("book_tickets", event_slug)
            else:
                reservation = form.save(commit=False)
                event.remaining_tickets = event.max_capacity - reservation.num_tickets
                reservation.guest = request.user
                reservation.event = event
                reservation.event_date = event.date
                reservation.event_time = event.time
                reservation.save()
                event.save()
                messages.success(request, f"You have successfully booked {reservation.num_tickets} seats for the {event.name}!")
                return redirect('dashboard', request.user.id)

    context = {
        'form': form,
        'event' : event,
    }
    return render(request, 'book_tickets.html', context)


class Signup(View):
    form_class = UserSignup
    template_name = 'signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            messages.success(request, "You have successfully signed up.")
            login(request, user)
            return redirect("home")
        messages.warning(request, form.errors)
        return redirect("signup")


class Login(View):
    form_class = UserLogin
    template_name = 'login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                messages.success(request, "Welcome Back!")
                return redirect('dashboard', request.user.id)
            messages.warning(request, "Wrong email/password combination. Please try again.")
            return redirect("login")
        messages.warning(request, form.errors)
        return redirect("login")


class Logout(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("login")
