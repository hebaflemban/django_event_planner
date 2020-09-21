from django.shortcuts import render
from rest_framework.generics import (ListAPIView)
from events.models import Event
from django.utils import timezone
from .serializers import EventListSerializer


class UpcomingEvents (ListAPIView):
    queryset = Event.objects.filter(date__gte = timezone.now())
    serializer_class = EventListSerializer
