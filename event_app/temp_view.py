from django.db.models import query
from django.shortcuts import get_list_or_404, render
from django.views.generic import CreateView, ListView
from .models import EventDetail, Attendant
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, get_list_or_404
from django.views.generic import TemplateView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AttendantListSerializer, EventListSerializer
from rest_framework import generics
# Create your views here.


class HomepageView(TemplateView):
    template_name = 'home.html'


def ListUser(request, event_uuid):
    event = get_object_or_404(EventDetail, id=event_uuid)
    # user = event.attendants.all()
    return render(request, 'register_user_list.html', {'event': event, })


class ListEventView(ListView):
    model = EventDetail
    template_name = 'list_event.html'
    context_object_name = 'events'


class CreateEventView(CreateView):
    model = EventDetail
    fields = "__all__"
    template_name = 'create_event.html'
    success_url = reverse_lazy('list_event')


# class EventList(APIView):
#     def get(self, request):
#         event = EventDetail.objects.all()
#         data = EventListSerializer(event, many=True).data
#         return Response(data)


# class AttendantList(APIView):
#     # queryset = Poll.objects.all()
#     def get(self, request, pk):
#         event = get_object_or_404(EventDetail, pk=pk)
#         event_attendant = event.attendants.all()
#         data = AttendantListSerializer(event_attendant, many=True).data
#         return Response(data)


urlpatterns = [
#     path('list/', views.EventList.as_view(), name='p_list'),
#     path('detail/<pk>/',
#          views.AttendantList.as_view(), name='p_detail'),
    path('', views.HomepageView.as_view(), name='home'),
    path('event/', views.ListEventView.as_view(), name='list_event'),
    path('event/create/', views.CreateEventView.as_view(), name='create_event'),
    path('event/<event_uuid>/', views.ListUser,
         name='attendance_list'),
]
