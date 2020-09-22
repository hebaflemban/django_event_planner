from rest_framework import serializers
from events.models import Event,Reservation, Connection
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
	password = serializers.CharField(write_only=True)
	class Meta:
		model = User
		fields = ['username', 'password', 'email']

	def create(self, validated_data):
		new_user = User(**validated_data)
		new_user.set_password(new_user.password)
		new_user.save()
		return validated_data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ]


class CreateEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude = ['created_by', 'slug', 'remaining_tickets']


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['name', 'created_by', 'date', ]


class BookedEventSerializer(serializers.ModelSerializer):
    event = EventListSerializer()
    class Meta:
        model = Reservation
        fields = [ 'event', 'num_tickets','reservation_date' ]


class BookEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [ 'num_tickets' ]


class EventReservationsSerializer(serializers.ModelSerializer):
    guest = UserSerializer()
    class Meta:
        model = Reservation
        fields = [ 'guest', 'num_tickets','reservation_date' ]


class FollowUserSerializer(serializers.ModelSerializer):
	class Meta:
		model = Connection
		fields = ['following_user']


class FollowingSeializer(serializers.ModelSerializer):
    following_user = UserSerializer()
    class Meta:
        model = Connection
        fields =[ 'following_user' ]
