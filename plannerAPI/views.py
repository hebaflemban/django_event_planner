from django.shortcuts import render
from rest_framework.generics import (ListAPIView)
from events.models import Event
from django.utils import timezone
from .serializers import EventListSerializer
from django.contrib.auth.models import User


class UpcomingEvents (ListAPIView):
    queryset = Event.objects.filter(date__gte = timezone.now())
    serializer_class = EventListSerializer


class OrganizerEvents (ListAPIView):
    serializer_class = EventListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'organizer_id'

    def get_queryset(self,):
        return Event.objects.filter(created_by = self.request.user)


class MyBookedEvents (ListAPIView):
    serializer_class = EventListSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'member_id'

    def get_queryset(self,):
        return self.request.user.events.all()
