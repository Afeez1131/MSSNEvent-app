from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('export_csv/<slug>/', views.export_all_attendant, name='export_csv'),

    path('export_csv/<slug>/<day>/', views.export_days_attendant, name='export_day_csv'),
    path('event/', views.event_list, name='event_list'),
    # list of all events
    path('event/<int:year>/', views.event_list_year, name='event_list_year'),
    # list of event by year
    path('event/create/', views.event_create, name='event_create'),
    # create new event
    path('attendant/<slug>/create/', views.create_attendant, name='attendant_create'),
    path('attendant/<slug>/', views.all_attendants, name='event_attendant'),
    path('all-attendants/', views.ajax_all_attendants),
    # return all attendant for an event with the slug passed in the url *args
    path('attendant/<slug>/<day>/', views.attendant_by_day, name='event_list_day'),
    # return the attendant for the day passed with the url *args
    path('dashboard/<slug:slug>/', views.dashboard_all, name='dashboard'),
    # create a new attendant
    path('dashboard/<slug:slug>/<day>/', views.dashboard, name='dashboard'),
    path('create-event-attendants', views.ajax_create_attendants),
    path('search-attendants/', views.search_attendant),
    path('fill-attendant-form/', views.fill_attendant_form),
    path('paginate/', views.ajax_paginate)
]
