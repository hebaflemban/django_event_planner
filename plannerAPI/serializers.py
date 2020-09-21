from rest_framework import serializers
from events.models import Event

class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'created_by', 'date', ]
