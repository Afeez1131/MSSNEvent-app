from django.core.management import BaseCommand

from event_app.models import EventDetail, Attendant


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        events = EventDetail.objects.all()
        for event in events:
            events = event.attendants.order_by('name').distinct('name', 'day', 'level', 'phone_number', 'department')
            duplicate_list = []
            ids = []
            for att in events:
                at = Attendant.objects.filter(name=att.name, day=att.day, level=att.level,
                                              phone_number=att.phone_number, department=att.department)
                if at.count() > 1:
                    for attendant in at[1:]:
                        attendant.delete()

        print('----------------done---------------')
