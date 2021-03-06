from django.urls import path
from .views import( Login, Logout, Signup, dashboard, home, event_details,
					events_list, update_event, create_event, book_tickets,
					update_profile, reservation_details
				)


urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),

	path('dashboard/<int:user_id>/', dashboard , name = 'dashboard' ),
	path('dashboard/<int:user_id>/edit', update_profile , name = 'update_profile' ),

	path('reservations/<int:reservation_id>/', reservation_details , name = 'reservation_details' ),

	path('events/', events_list , name='events_list'),
	path('events/create/', create_event , name='create_event'),
	path('events/<slug:event_slug>/details/', event_details , name='event_details'),
	path('events/<str:event_slug>/update/', update_event , name='update_event'),
	path('events/<str:event_slug>/book/', book_tickets , name='book_tickets'),

]
