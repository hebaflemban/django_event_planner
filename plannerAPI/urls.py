from django.urls import path
from .views import (
	UpcomingEvents, OrganizerEvents, MyBookedEvents, OrganizersIFollow,
	SignupAPI, CreateEvent , ModifyEvent, EventReservations, BookEvent, FollowUser
	)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
	)

urlpatterns = [

    path('api/signup/', SignupAPI.as_view(), name='api_sigup'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),

    path('events/cteate/', CreateEvent.as_view() , name='create_event'),
    path('events/modify/<int:event_id>/', ModifyEvent.as_view() , name='modify_event'),
    path('events/book/<int:event_id>/', BookEvent.as_view() , name='book_event'),

    path('events/upcoming/', UpcomingEvents.as_view() , name='upcoming_events'),
	path('events/booked/<int:member_id>/', MyBookedEvents.as_view() , name='my_booked_events'),
    path('events/reservations/<int:event_id>/', EventReservations.as_view() , name='event_reservations'),
    path('events/byorgnaizer/', OrganizerEvents.as_view() , name='organizer_events'),

	path('follow/', FollowUser.as_view() , name='follow_user'),
    path('followings/', OrganizersIFollow.as_view() , name='organizers_i_follow'),

]
