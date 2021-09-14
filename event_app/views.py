from django.http.response import Http404
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from .models import EventDetail, Attendant, Year
from .forms import AttendantCreateForm, EventCreateForm
from datetime import datetime
import json
import csv
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.template import RequestContext


def handler404(request, *args, **argv):
    response = render('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def HomePageView(request):
    template_name = 'home.html'

    recent_event = EventDetail.objects.all()[:4]
    return render(request, template_name, {'recent_event': recent_event, })

# event function start


def EventList(request):
    events = EventDetail.objects.all()

    return render(request, 'event_list.html', {'events': events, })


def EventListViewByYear(request, year):
    # events = get_object_or_404(EventDetail, year=year)
    try:
        year_instance = Year.objects.get(year=year)
        events = EventDetail.objects.filter(year=year_instance)
    except Exception as DoesNotExist:
        year_instance = year
        events = ''
    return render(request, 'event_list_year.html', {'events': events, 'year_instance': year_instance, })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def EventCreateView(request):
    if request.method == 'POST':
        form = EventCreateForm(request.POST)
        if form.is_valid():
            form_year = form.cleaned_data['year'] = datetime.now().year
            year = get_object_or_404(Year, year=form_year)
            f = form.save(commit=False)
            f.year = year
            f.save()
            return redirect('event_list')
    else:
        form = EventCreateForm()
    return render(request, 'event_create.html', {'form': form, })


# event function end
@login_required
@user_passes_test(lambda u: u.is_superuser)
def export_all_attendant(request, slug):
    events = get_object_or_404(EventDetail, slug=slug)
    attendants = Attendant.objects.all().filter(eventdetail=events)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="%s-all-attendants.csv"' % (
        events.slug)

    writer = csv.writer(response)
    writer.writerow(['day', 'name', 'level', 'phone_number',
                    'visitor', 'department', 'sex', 'email'])

    attendants_csv = attendants.values_list(
        'day', 'name', 'level', 'phone_number', 'visitor', 'department', 'sex', 'email')
    for att in attendants_csv:
        writer.writerow(att)

    return response


@login_required
@user_passes_test(lambda u: u.is_superuser)
def export_days_attendant(request, slug, day):
    events = get_object_or_404(EventDetail, slug=slug)

    try:

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s-%s-attendants.csv"' % (
            events.slug, day)

        writer = csv.writer(response)
        writer.writerow(['day', 'name', 'level', 'phone_number',
                        'visitor', 'department', 'sex', 'email'])
        attendants = Attendant.objects.filter(eventdetail=events, day=day).values_list(
            'day', 'name', 'level', 'phone_number', 'visitor', 'department', 'sex', 'email')
        for att in attendants:
            writer.writerow(att)

    except Exception as e:
        return Http404
    return response


# attendant function start

@login_required
@user_passes_test(lambda u: u.is_superuser)
def EventAllAttendant(request, slug):

    events = get_object_or_404(EventDetail, slug=slug)
    attendants = Attendant.objects.all().filter(eventdetail=events)
    paginator = Paginator(attendants, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    day_list = []
    for att in page_obj:
        if att.day in day_list:
            pass
        else:
            day_list.append(att.day)

    day_list.sort()
    return render(request, 'event_detail.html', {'attendants': attendants,
                                                 'events': events, 'page_obj': page_obj,
                                                 'day_list': day_list,
                                                 })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def AttendantByDay(request, slug, day):
    events = get_object_or_404(EventDetail, slug=slug)

    try:
        # attendants = Attendant.objects.filter(Q(eventdetail=events) & Q(day=day))
        attendants = get_list_or_404(Attendant, eventdetail=events, day=day)
        paginator = Paginator(attendants, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        events = ''
        attendants = ''
        page_obj = ''
    return render(request, 'event_day_detail.html', {'page_obj': page_obj, 'events': events, 'day': day,
                                                     })


def AttendantCreateView(request, slug):
    eventdetail = get_object_or_404(EventDetail, slug=slug)
    name = None
    if request.method == 'POST':
        form = AttendantCreateForm(request.POST)
        if form.is_valid():
            form.cleaned_data['attendants'] = eventdetail
            day = form.cleaned_data['day']
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']

            if Attendant.objects.filter(day=day, name=name, email=email).exists():
                messages.warning(request, 'Data exist before in the database')
            else:
                f = form.save(commit=False)
                f.eventdetail = eventdetail
                f.save()
                return redirect('event_list_day', day=day, slug=slug)
    else:
        form = AttendantCreateForm()
    return render(request, 'attendant_create.html', {'form': form, 'name': name})

# attendant function end


# dashboard function start

@login_required
@user_passes_test(lambda u: u.is_superuser)
def DashboardView(request, slug, day):
    labels = ["jan", "feb", "mar", "apr"]
    data = [100, 300, 300, 200]

    event_detail = get_object_or_404(EventDetail, slug=slug)
    try:
        attendants = Attendant.objects.filter(
            eventdetail=event_detail, day=day)
        all_attendants = Attendant.objects.filter(
            eventdetail=event_detail, day=day).count()
        male_count = attendants.filter(sex='brother').count()
        female_count = attendants.filter(sex='sister').count()
        visitor = attendants.filter(visitor='yes').count()

    except Exception as DoesNotExist:
        attendants = ''
        all_attendants = ''

    return render(request, 'dashboard.html', {'all_attendants': all_attendants,
                                              'day': day,
                                              'male_count': male_count,
                                              'female_count': female_count,
                                              'visitor': visitor,
                                              'event_detail': event_detail,
                                              'attendants': attendants,
                                              "collapse": "",
                                              "labels": json.dumps(labels),
                                              "data": json.dumps(data), })


@login_required
@user_passes_test(lambda u: u.is_superuser)
def DashboardViewAll(request, slug):
    labels = ["jan", "feb", "mar", "apr"]
    data = [100, 300, 300, 200]

    event_detail = get_object_or_404(EventDetail, slug=slug)
    try:
        attendants = Attendant.objects.filter(
            eventdetail=event_detail)
        all_attendants = Attendant.objects.filter(
            eventdetail=event_detail).count()
        male_count = attendants.filter(sex='brother').count()
        female_count = attendants.filter(sex='sister').count()
        visitor = attendants.filter(visitor='yes').count()

    except Exception as DoesNotExist:
        attendants = ''
        all_attendants = ''

    return render(request, 'dashboard.html', {'all_attendants': all_attendants,
                                              'male_count': male_count,
                                              'female_count': female_count,
                                              'visitor': visitor,
                                              'event_detail': event_detail,
                                              'attendants': attendants,
                                              "collapse": "",
                                              "labels": json.dumps(labels),
                                              "data": json.dumps(data), })
