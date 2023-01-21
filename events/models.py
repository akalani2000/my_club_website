from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Number', max_length=15, blank=True)
    web = models.URLField('Website', blank=True)
    email_address = models.EmailField('Email', blank=True)
    owner = models.IntegerField("Venue Owner", blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name


class MyClubUser(models.Model):
    first_name = models.CharField('First Name', max_length=50)
    last_name = models.CharField('Last Name', max_length=50)
    email = models.EmailField('Email')

    def __str__(self):
        return self.first_name + ' ' + self.last_name


class Event(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # venue = models.CharField('Event Venue', max_length=50)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)
    approved = models.BooleanField('Approved', default=False)

    def __str__(self):
        return self.name

    @property
    def days_till(self):
        today = date.today()
        days = self.event_date.date() - today
        days_t = str(days).split(',', 1)[0]
        return days_t

    @property
    def is_past(self):
        today = date.today()
        if self.event_date.date() < today:
            thing = "Ended"
        elif self.event_date.date() == today:
            thing = "Running"
        else:
            thing = "In Future"
        return thing
