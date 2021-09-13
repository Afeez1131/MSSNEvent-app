from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomePageView, name='home'),

    path('export_csv/<slug>/', views.export_all_attendant, name='export_csv'),

    path('export_csv/<slug>/<day>/',
         views.export_days_attendant, name='export_day_csv'),


    path('event/', views.EventList, name='event_list'),
    # list of all events
    path('event/<int:year>/', views.EventListViewByYear, name='event_list_year'),
    # list of event by year
    path('event/create/', views.EventCreateView, name='event_create'),
    # create new event

    path('attendant/<slug>/create/',
         views.AttendantCreateView, name='attendant_create'),

    path('attendant/<slug>/',
         views.EventAllAttendant, name='event_attendant'),
    # return all attendant for an event with the slug passed in the url *args
    path('attendant/<slug>/<day>/',
         views.AttendantByDay, name='event_list_day'),
    # return the attendant for the day passed with the url *args

    path('dashboard/<slug:slug>/', views.DashboardViewAll, name='dashboard'),

    # create a new attendant

    path('dashboard/<slug:slug>/<day>/',
         views.DashboardView, name='dashboard'),


]
