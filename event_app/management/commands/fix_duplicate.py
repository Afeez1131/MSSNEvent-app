from django.core.management import BaseCommand

from event_app.models import EventDetail, Attendant


class Command(BaseCommand):
    def handler(self, *args, **kwargs):
        events = EventDetail.objects.all()
        duplicate_list = []
        for event in events:
            attendants = event.attendants.all()
            for att in attendants:
                name = att.name
                phone = att.phone_number
                day = att.day
                level = att.level
                atts = attendants.filter(name=name, phone_number=phone,
                                         day=day, level=level)
                if atts.count() > 1:
                    # atts[1:].delete()
                    print('duplicate attendants: ', atts.name, atts.day, atts.level)
        print('----------------done---------------')
