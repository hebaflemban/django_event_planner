from django.urls import path
from .views import(UpcomingEvents, OrganizerEvents, MyBookedEvents )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('events/upcoming/', UpcomingEvents.as_view() , name='UpcomingEvents'),
    path('events/<int:organizer_id>/', OrganizerEvents.as_view() , name='OrganizerEvents'),
    path('events/<int:organizer_id>/', MyBookedEvents.as_view() , name='MyBookedEvents'),

]
