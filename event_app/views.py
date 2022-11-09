from django.db.utils import IntegrityError
from django.http.response import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.urls import reverse

from .models import EventDetail, Attendant, Year
from .forms import AttendantCreateForm, EventCreateForm
from datetime import datetime
import json
import csv
from django.contrib import messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from django.template import RequestContext


def handler404(request, *args, **argv):
    response = render('404.html', {}, context_instance=RequestContext(request))
    response.status_code = 404
    return response


def home(request):
    template_name = 'home.html'

    recent_event = EventDetail.objects.all()[:4]
    return render(request, template_name, {'recent_event': recent_event, })


# event function start

@login_required()
def event_list(request):
    events = EventDetail.objects.all()
    return render(request, 'event_list.html', {'events': events, })


def event_list_year(request, year):
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
def event_create(request):
    if request.method == 'POST':
        form = EventCreateForm(request.POST)
        if form.is_valid():
            event_year = datetime.now().year
            year, _ = Year.objects.get_or_create(year=event_year)
            f = form.save(commit=False)
            f.year = year
            f.save()
            return HttpResponseRedirect(reverse('event_list'))
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
        pass
    return response


# attendant function start

@login_required
@user_passes_test(lambda u: u.is_superuser)
def all_attendants(request, slug):
    event = get_object_or_404(EventDetail, slug=slug)
    attendants = event.attendants.all().order_by('-id')
    paginator = Paginator(attendants, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print('page number: ', page_obj)

    return render(request, 'event_detail.html', {'attendants': attendants,
                                                 'event': event, 'page_obj': page_obj})


def reload_attendants(request, event, slug, day=None):
    if day:
        attendants = event.attendants.filter(day=day)
    else:
        attendants = event.attendants.all().order_by('-id')
    paginator = Paginator(attendants, 20)
    page_number = request.GET.get('page')
    attendants = paginator.get_page(page_number)
    attendants = [attendant for attendant in attendants]
    out = []
    for i in range(len(attendants)):
        counter = i + 1
        att = attendants[i]
        url = reverse('event_attendant', args=[slug])
        day_url = reverse('event_list_day', args=[slug, att.day])
        if not day:
            d = f'''<tr><td>{counter}</td><td>{att.name}</td><td>{att.level}</td><td>{att.phone_number}</td><td>{att.visitor}</td><td>{att.sex}</td><td>{att.department}</td><td>{att.email}</td><td><a href="{day_url}">{att.day}</a></td></tr>'''
        else:
            d = f'''<tr><td>{counter}</td><td>{att.name}</td><td>{att.level}</td><td>{att.phone_number}</td><td>{att.visitor}</td><td>{att.sex}</td><td>{att.department}</td><td>{att.email}</td><td>{att.day}</td></tr>'''
        out.append(d)
    fout = ''.join(out)
    return fout

from django.template.loader import render_to_string
def ajax_paginate(request):
    slug = request.GET.get('slug')
    day = request.GET.get('day') or None
    out = []
    if not day:
        event = EventDetail.objects.get(slug=slug)
    else:
        event = EventDetail.objects.get(slug=slug, day=day)
    attendants = event.attendants.all()
    paginator = Paginator(attendants, 10)
    page = request.GET.get('page')
    try:
        attendants = paginator.page(page)
    except PageNotAnInteger:
        attendants = paginator.page(1)
    except EmptyPage:
        attendants = paginator.page(paginator.num_pages)
    pagination = render_to_string('pagination.html', {'page_obj': attendants})
    for i in range(len(attendants)):
        counter = i + 1
        att = attendants[i]
        url = reverse('event_attendant', args=[slug])
        day_url = reverse('event_list_day', args=[slug, att.day])
        if not day:
            d = f'''<tr><td>{counter}</td><td>{att.name}</td><td>{att.level}</td><td>{att.phone_number}</td><td>{att.visitor}</td><td>{att.sex}</td><td>{att.department}</td><td>{att.email}</td><td><a href="{day_url}">{att.day}</a></td></tr>'''
        else:
            d = f'''<tr><td>{counter}</td><td>{att.name}</td><td>{att.level}</td><td>{att.phone_number}</td><td>{att.visitor}</td><td>{att.sex}</td><td>{att.department}</td><td>{att.email}</td><td>{att.day}</td></tr>'''
        out.append(d)
    fout = ''.join(out)
    return JsonResponse({'attendants': fout, 'pagination': pagination})


def ajax_all_attendants(request):
    slug = request.GET.get('slug')
    day = request.GET.get('day') or None
    event = EventDetail.objects.get(slug=slug)
    return JsonResponse({'attendants': reload_attendants(request, event, slug, day)})


@login_required
@user_passes_test(lambda u: u.is_superuser)
def attendant_by_day(request, slug, day):
    events = get_object_or_404(EventDetail, slug=slug)
    try:
        # attendants = Attendant.objects.filter(Q(eventdetail=events) & Q(day=day))
        attendants = get_list_or_404(Attendant, eventdetail=events, day=day)
        paginator = Paginator(attendants, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
    except Exception as e:
        events = ''
        attendants = ''
        page_obj = ''
    return render(request, 'event_day_detail.html', {'page_obj': page_obj, 'events': events, 'day': day,
                                                     })


def create_attendant(request, slug):
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
    return render(request, 'attendant_create.html', {'form': form, 'name': name, 'slug': eventdetail.slug})


def ajax_create_attendants(request):
    day = request.POST.get('day')
    name = request.POST.get('name')
    level = request.POST.get('level')
    phone_number = request.POST.get('phone_number')
    visitor = request.POST.get('visitor')
    department = request.POST.get('department')
    email = request.POST.get('email')
    sex = request.POST.get('sex')
    slug = request.POST.get('event_slug')
    try:
        event = EventDetail.objects.get(slug=slug)
        Attendant.objects.create(eventdetail=event, day=day, name=name,
                                 level=level, phone_number=phone_number, visitor=visitor,
                                 department=department, email=email, sex=sex)
    except IntegrityError as ie:
        return JsonResponse({'exception': 'Duplicate entry not allowed.'})
    except Exception as e:
        return JsonResponse({'servererror': 'An internal serval error, kindly try again.'})

    return JsonResponse({'success': 'Okay'})


# attendant function end


# dashboard function start

@login_required
@user_passes_test(lambda u: u.is_superuser)
def dashboard(request, slug, day):
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
def dashboard_all(request, slug):
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
