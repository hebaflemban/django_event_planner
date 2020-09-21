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
from .forms import UserSignup, UserLogin, EventForm, ReservationForm
from .models import Event, Connection, Tag, Reservation


def home(request):
    return render(request, 'home.html')


def events_list(request):
    events = Event.objects.filter(date__gte = timezone.now())
    context = {
        'events': events
    }
    return render(request, 'events_list.html', context)


def event_details(request, event_slug):
    event = Event.objects.get(slug = event_slug)
    reservations = event.reservations.all()
    print(reservations)
    context = {
        "event" : event,
        "reservations" : reservations
    }
    return render(request, 'event_details.html', context)



def create_event(request):
    if not request.user.is_authenticated:
        messages.warning(request, "messages : You don\'t have access ")
        raise Http404('You don\'t have access ')
    organizer = User.objects.get(id=request.user.id)
    form = EventForm()
    if request.method == "POST":
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            event = form.save(commit=False)
            event.created_by = organizer
            event.save()
            event.save_m2m()
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
            reservation = form.save(commit=False)
            event.remaining_tickets = event.max_capacity - reservation.num_tickets
            reservation.guest = request.user
            reservation.event = event
            reservation.date = event.date
            reservation.save()
            messages.success(request, f"You have successfully booked {reservation.num_tickets} seats for the {event.name}!")

            return redirect('dashboard', request.user.id)

    context = {
        'form': form,
        'event' : event,
    }
    return render(request, 'book_tickets.html', context)


def search(request):
    search_result = None
    search_term = None
    if 'search_events' in request.GET:
        search_term = request.GET['search_events']
        search_result = Event.objects.all().filter(Q(name__icontains=search_term) |
                        Q(description__icontains=search_term) | Q(created_by__username__icontains=search_term))

    context = {
        'search_term' : search_term,
        'search_result' : search_result
    }

    return render(request, 'search.html', context)



class Dashboard(View):
    model = User
    slug_field = 'username'
    template_name = 'dashboard.html'

    def get(self, request, *args, **kwargs):
        print(request.user.reservations.filter(date__gte = timezone.now()))
        context = {
            "user": request.user,
            "followers" : request.user.followers.count(),
            "following" : request.user.following.count(),
            "myevents" : request.user.MyEvents.all(),
            "upcoming_resevations" : request.user.reservations.filter(date__gte = timezone.now()),
            "past_reservations" : request.user.reservations.filter(date__lt = timezone.now())
        }
        return render (request, self.template_name, context)

def create_user_slug(instance, new_slug=None):
    slug = slugify(instance.username)
    if new_slug is not None:
        slug = new_slug
    qs = User.objects.filter(slug=slug)
    if qs.exists():
        try:
            int(slug[-1])
            if "-" in slug:
                slug_list = slug.split("-")
                new_slug = "%s%s" % (slug[:-len(slug_list[-1])], int(slug_list[-1]) + 1)
            else:
                new_slug = "%s-1" % (slug)
        except:
            new_slug = "%s-1" % (slug)
        return create_slug(instance, new_slug=new_slug)
    return slug


@receiver(pre_save, sender=Dashboard)
def generate_slug(instance, *args, **kwargs):
    if not instance.slug_field:
        instance.slug_field=create_user_slug(instance)



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
