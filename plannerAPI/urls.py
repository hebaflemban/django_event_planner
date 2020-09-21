from django.urls import path
from .views import(UpcomingEvents )

urlpatterns = [
    path('events/upcoming/', UpcomingEvents.as_view() , name='UpcomingEvents'),

]
