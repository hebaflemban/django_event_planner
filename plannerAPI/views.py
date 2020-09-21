from django.shortcuts import render
from django.utils import timezone
from django.contrib.auth.models import User
from rest_framework.generics import (ListAPIView)
from rest_framework.permissions import IsAuthenticated
from events.models import Event, Connection
from .serializers import EventListSerializer, BookedEventSerializer, UserSerializer, FollowingSeializer


class UpcomingEvents (ListAPIView):
    queryset = Event.objects.filter(date__gte = timezone.now())
    serializer_class = EventListSerializer


class OrganizerEvents (ListAPIView):
    serializer_class = EventListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'organizer_id'
    permission_classes = [IsAuthenticated]


    def get_queryset(self,):
        if self.request.user.id == self.kwargs['organizer_id']:
            return Event.objects.filter(created_by = self.request.user)


class MyBookedEvents (ListAPIView):
    serializer_class = BookedEventSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'member_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self,):
        if self.request.user.id == self.kwargs['member_id']:
            return self.request.user.reservations.all()


class OrganizersIFollow(ListAPIView):
    serializer_class = FollowingSeializer
    lookup_field = 'id'
    lookup_url_kwarg = 'member_id'
    permission_classes = [IsAuthenticated]

    def get_queryset(self,):
        if self.request.user.id == self.kwargs['member_id']:
            return self.request.user.following.all()
