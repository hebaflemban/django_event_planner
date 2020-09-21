from django.urls import path
from .views import(UpcomingEvents, OrganizerEvents, MyBookedEvents, OrganizersIFollow )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('events/upcoming/', UpcomingEvents.as_view() , name='upcoming-events'),
    path('events/<int:organizer_id>/', OrganizerEvents.as_view() , name='organizer-events'),
    path('events/booked/<int:member_id>/', MyBookedEvents.as_view() , name='my-booked-events'),
    path('followings/<int:member_id>/', OrganizersIFollow.as_view() , name='organizers-i-follow'),

]
