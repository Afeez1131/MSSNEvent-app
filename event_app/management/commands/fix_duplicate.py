from django.core.management import BaseCommand

from event_app.models import EventDetail, Attendant


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        events = EventDetail.objects.all()
        for event in events:
            attendants = event.attendants.all()
            duplicate_list = []
            ids = []

            for att in attendants:
                name = att.name
                phone = att.phone_number
                day = att.day
                level = att.level
                atts = attendants.filter(name=name, phone_number=phone,
                                         day=day, level=level)
                if atts.count() > 1:
                    for item in atts:
                        duplicate_list.append(item)
                        ids.append(item.id)
                    # atts[1:].delete()
                    print('duplicate list: ', duplicate_list)
                    print('id list: ', ids)


        print('----------------done---------------')
