from rest_framework import serializers
from events.models import Event,Reservation, Connection
from django.contrib.auth.models import User


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'created_by', 'date', ]


class BookedEventSerializer(serializers.ModelSerializer):
    event = EventListSerializer()
    class Meta:
        model = Reservation
        fields = [ 'event', 'num_tickets','reservation_date' ]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ]


class FollowingSeializer(serializers.ModelSerializer):
    following_user = UserSerializer()
    class Meta:
        model = Connection
        fields =[ 'following_user' ]
