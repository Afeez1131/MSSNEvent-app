from django.contrib import admin
from django.contrib.admin.options import TabularInline
from .models import EventDetail, Attendant, Year
# Register your models here.


class AdminAttendant(admin.TabularInline):
    model = Attendant
    max_num = 1
    extra = 0


class AttendantAdmin(admin.ModelAdmin):
    search_fields = ['phone_number', 'name']


class EventDetailAdmin(admin.ModelAdmin):
    list_display = ['event_name', 'date', 'slug']
    inlines = [
        AdminAttendant
    ]
    readonly_fields = ('date',)




admin.site.register(EventDetail, EventDetailAdmin)
admin.site.register(Attendant)
admin.site.register(Year)
