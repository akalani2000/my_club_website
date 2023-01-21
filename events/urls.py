from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events', views.all_events, name='list-events'),
    path('add_venue', views.add_venue, name='add-venue'),
    path('list_venues', views.list_venues, name='list-venues'),
    path('show_venue/<venue_id>', views.show_venue, name='show-venue'),
    path('update_venue/<venue_id>', views.update_venue, name='update-venue'),
    path('search_venues', views.search_venues, name='search-venues'),
    path('add_event', views.add_event, name='add-event'),
    path('update_events/<event_id>', views.update_events, name='update-events'),
    path('delete_events/<event_id>', views.delete_event, name='delete-event'),
    path('delete_venue/<venue_id>', views.delete_venue, name='delete-venue'),
    path('venue_text', views.venue_text, name='venue-text'),
    path('event_text', views.event_text, name='event-text'),
    path('venue_csv', views.venue_csv, name='venue-csv'),
    path('event_csv', views.event_csv, name='event-csv'),
    path('venue_pdf', views.venue_pdf, name='venue-pdf'),
    path('event_pdf', views.event_pdf, name='event-pdf'),
    path('my_event', views.my_event, name='my-event'),
    path('search_event', views.search_event, name='search-event'),
    path('admin_approval', views.admin_approval, name='admin-approval'),
    path('venue_event/<venue_id>', views.venue_event, name='venue-event'),
    path('show_event/<event_id>', views.show_event, name='show-event'),
]
