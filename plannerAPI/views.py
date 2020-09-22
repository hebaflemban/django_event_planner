from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.generics import (ListAPIView, CreateAPIView, RetrieveUpdateAPIView)
from rest_framework.permissions import IsAuthenticated
from events.models import Event, Connection, Reservation
from .serializers import (
    EventListSerializer, BookedEventSerializer, UserSerializer, FollowingSeializer,
    RegisterSerializer, CreateEventSerializer, EventReservationsSerializer,
    BookEventSerializer, BookedEventSerializer, BookedEventSerializer,
    FollowUserSerializer
    )


class SignupAPI(CreateAPIView):
    serializer_class = RegisterSerializer


class CreateEvent(CreateAPIView):
    serializer_class = CreateEventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, remaining_tickets = max_capacity)


class ModifyEvent(RetrieveUpdateAPIView):
	queryset = Event.objects.all()
	serializer_class = CreateEventSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'event_id'
	permission_classes = [IsAuthenticated]


class BookEvent(CreateAPIView):
    serializer_class = BookEventSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        event = Event.objects.get(id = self.kwargs['event_id'])
        serializer.save(event=event, guest = self.request.user, date = event.date)


class UpcomingEvents (ListAPIView):
    queryset = Event.objects.filter(date__gte = timezone.now())
    serializer_class = EventListSerializer


class OrganizerEvents (ListAPIView):
    serializer_class = EventListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self,):
        return Event.objects.filter(created_by = self.request.user)


class MyBookedEvents (ListAPIView):
    serializer_class = BookedEventSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'member_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self,):
        if self.request.user.id == self.kwargs['member_id']:
            return self.request.user.reservations.all()


class EventReservations(ListAPIView):
    serializer_class = EventReservationsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self,):
        event = Event.objects.get(id = self.kwargs['event_id'])
        if self.request.user == event.created_by:
            return Reservation.objects.filter(event = event)


class FollowUser(CreateAPIView):
    serializer_class = FollowUserSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class OrganizersIFollow(ListAPIView):
    serializer_class = FollowingSeializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self,):
        return self.request.user.following.all()
