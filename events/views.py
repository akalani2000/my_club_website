from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Event, Venue
# Django user model
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

from django.core.paginator import Paginator


# show individual event
def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/show_event.html', {'event': event})


# venue wise events
def venue_event(request, venue_id):
    # venue filter
    venue = Venue.objects.get(id=venue_id)
    # venue related events
    events = venue.event_set.all()
    return render(request, 'events/venue_event.html', {'events': events})


# admin approve the events
def admin_approval(request):
    # Get the venues
    venues = Venue.objects.all()
    # Get counts
    event_count = Event.objects.all().count()
    venue_count = Venue.objects.all().count()
    user_count = User.objects.all().count()
    events = Event.objects.all().order_by('-event_date')
    if request.user.is_superuser:
        if request.method == 'POST':
            id_list = request.POST.getlist('check1')
            # clear all checkbox
            events.update(approved=False)
            # Update the database
            for i in id_list:
                Event.objects.filter(pk=i).update(approved=True)
            messages.success(request, 'Event list Approval has been updated!.')
            return redirect('list-events')
        else:
            return render(request, 'events/admin_approval.html', {'events': events,
                                                                  'event_count': event_count,
                                                                  'venue_count': venue_count,
                                                                  'user_count': user_count,
                                                                  'venues': venues})
    else:
        messages.error(request, 'You cannot access this page.')
        return redirect('home')


# search the events
def search_event(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = searched.capitalize()
        events = Event.objects.filter(name__contains=searched)
        return render(request, 'events/search_event.html', {'searched': searched, 'events': events})
    else:
        return render(request, 'events/search_event.html', {})


# Listing My events
def my_event(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)
        return render(request, 'events/my_events.html', {'events': events})
    else:
        messages.error(request, "Your are not authorize to view this page.")
        return redirect('home')


# Create your views here.
def venue_pdf(request):
    # create a Bytestream Buffer
    buf = io.BytesIO()
    # create a canves
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    venues = Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(" ")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='venues.pdf')


def event_pdf(request):
    # create a Bytestream Buffer
    buf = io.BytesIO()
    # create a canves
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    events = Event.objects.all()
    lines = []
    for event in events:
        lines.append(event.name)
        lines.append(event.event_date)
        lines.append(event.venue)
        lines.append(event.manager)
        lines.append(event.attendees)
        lines.append(event.description)
        lines.append(" ")

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)
    return FileResponse(buf, as_attachment=True, filename='events.pdf')


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'
    # csv writer
    writer = csv.writer(response)
    venues = Venue.objects.all().order_by('name')
    # setting up the headings for the csv file
    writer.writerow(['Venue Name', 'Address', 'Zipcode', 'Phone Number', 'Website', 'Email Address'])
    lines = []
    for venue in venues:
        writer.writerow([venue,
                         venue.address,
                         venue.zip_code,
                         venue.phone,
                         venue.web,
                         venue.email_address])
    return response


def event_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=events.csv'
    events = Event.objects.all().order_by('name')
    writer = csv.writer(response)
    # setting up the headings for the csv file
    writer.writerow(
        ['Event Name', 'Event Date', 'Event Venue', 'Event Manager', 'Event Attendees', 'Event Description'])

    for event in events:
        writer.writerow([event,
                         event.event_date,
                         event.venue,
                         event.manager,
                         event.attendees,
                         event.description])
    return response


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'
    venues = Venue.objects.all().order_by('name')
    lines = []
    for venue in venues:
        lines.append(f'{venue}\n'
                     f'{venue.address}\n'
                     f'{venue.zip_code}\n'
                     f'{venue.phone}\n'
                     f'{venue.web}\n'
                     f'{venue.email_address}\n\n')
    response.writelines(lines)
    return response


def event_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=events.txt'
    events = Event.objects.all().order_by('name')
    lines = []
    for event in events:
        lines.append(f'{event}\n'
                     f'{event.event_date}\n'
                     f'{event.venue}\n'
                     f'{event.manager}\n'
                     f'{event.attendees}\n'
                     f'{event.description}\n\n')
    response.writelines(lines)
    return response


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if event.manager == request.user:
        event.delete()
        return redirect('list-events')
    else:
        messages.error(request, "Your are not authorize to delete this event")
        return redirect('list-events')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    if venue.owner == request.user.id:
        venue.delete()
        return redirect('list-venues')
    else:
        messages.error(request, "Your are not authorize to delete this venue")
        return redirect('list-venues')


def add_event(request):
    submitted = False
    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')
    else:
        if request.user.is_superuser:
            form = EventFormAdmin
        else:
            form = EventForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_events(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')
    return render(request, 'events/update_events.html', {'event': event, 'form': form})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        return redirect('list-venues')
    return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})


def search_venues(request):
    if request.method == "POST":
        searched = request.POST['searched']
        searched = searched.capitalize()
        venues = Venue.objects.filter(name__contains=searched)
        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues})
    else:
        return render(request, 'events/search_venues.html', {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)

    events = venue.event_set.all()
    return render(request, 'events/show_venue.html', {'venue': venue, 'venue_owner': venue_owner, 'events': events})


def list_venues(request):
    venue_list = Venue.objects.all().order_by('name')

    # set up pagination
    p = Paginator(Venue.objects.all().order_by('name'), 5)
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = 'a' * venues.paginator.num_pages
    return render(request, 'events/venue.html', {'venue_list': venue_list, 'venues': venues, 'nums': nums})


def add_venue(request):
    submitted = False
    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            return HttpResponseRedirect('/add_venue?submitted=True')

    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def all_events(request):
    event_list = Event.objects.all().order_by('-event_date')
    return render(request, 'events/event_list.html', {'event_list': event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    # Convert the name of the month to number
    month = month.capitalize()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)

    # Query the events model for dates
    event_list = Event.objects.filter(
        event_date__year=year,
        event_date__month=month_number,
    )

    now = datetime.now()
    current_year = now.year
    time = now.strftime('%H:%M:%S %p')

    return render(request, 'events/home.html', {
        'year': year,
        'month': month,
        'month_number': month_number,
        'cal': cal,
        'now': now,
        'current_year': current_year,
        'time': time,
        'event_list': event_list,
    })
