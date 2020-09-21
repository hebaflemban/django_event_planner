from django.contrib import admin
from .models import Tag, Event, Connection, Reservation


admin.site.register(Tag)
admin.site.register(Event)
admin.site.register(Connection)
admin.site.register(Reservation)
