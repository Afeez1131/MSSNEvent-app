from rest_framework import serializers
from .models import Attendant, EventDetail


class EventListSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventDetail
        fields = '__all__'


class AttendantListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendant
        fields = '__all__'
