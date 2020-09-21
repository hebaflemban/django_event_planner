from django.urls import path
from .views import( Login, Logout, Signup, Dashboard, home, event_details,
					events_list, update_event, create_event, book_tickets)

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

	#path('meetup/<str:slug>/', Dashboard.as_view() , name = 'dashboard' ),
	path('meetup/<int:user_id>/', Dashboard.as_view() , name = 'dashboard' ),
	path('events/', events_list , name='events_list'),
	path('events/create/', create_event , name='create_event'),
	path('events/<slug:event_slug>/details/', event_details , name='event_details'),
	path('events/<str:event_slug>/update/', update_event , name='update_event'),
	path('events/<str:event_slug>/book/', book_tickets , name='book_tickets'),

]
