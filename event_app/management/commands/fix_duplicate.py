from django.core.management import BaseCommand

from event_app.models import EventDetail, Attendant


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        events = EventDetail.objects.all()
        duplicate_list = []
        for event in events:
            attendants = event.attendants.order_by('name', 'level', 'phone_number', 'id').distinct('name', 'phone_number', 'level')
            print(attendants)
            for att in attendants:
                name = att.name
                phone = att.phone_number
                day = att.day
                level = att.level
                atts = attendants.filter(name=name, phone_number=phone,
                                         day=day, level=level)
                if atts.count() > 1:
                    # atts[1:].delete()
                    print('duplicate attendants: ', atts, atts.count())
                    print('after first: ', atts[1:])

        print('----------------done---------------')
