from django import forms
from django.forms import ModelForm
from .models import Venue, Event


class VenueForm(ModelForm):
    class Meta:
        model = Venue
        fields = ('name', 'address', 'zip_code', 'phone', 'web', 'email_address', 'venue_image')

        labels = {
            'name': '',
            'address': '',
            'zip_code': '',
            'phone': '',
            'web': '',
            'email_address': '',
            'venue_image': ''
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Venue name*'
                }
            ),
            'address': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Address*'
                }
            ),
            'zip_code': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Zip-code*'
                }
            ),
            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Phone'
                }
            ),
            'web': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Website address'
                }
            ),
            'email_address': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Email address'
                }
            ),
        }


# Admin superuser event form
class EventFormAdmin(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description', 'approved')

        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS ',
            'venue': 'Venues',
            'manager': 'Manager',
            'attendees': 'Attendees',
            'description': ''
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Event name*'
                }
            ),
            'event_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Event date'
                }
            ),
            'venue': forms.Select(
                attrs={
                    'class': 'form-select',
                    'placeholder': 'Venue name*'
                }
            ),
            'manager': forms.Select(
                attrs={
                    'class': 'form-select',
                    'placeholder': 'Manager name'
                }
            ),
            'attendees': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Attendees'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Description'
                }
            )
        }


# Normal User event form
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ('name', 'event_date', 'venue', 'attendees', 'description')

        labels = {
            'name': '',
            'event_date': 'YYYY-MM-DD HH:MM:SS ',
            'venue': 'Venues',
            'attendees': 'Attendees',
            'description': ''
        }
        widgets = {
            'name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Event name*'
                }
            ),
            'event_date': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Event date'
                }
            ),
            'venue': forms.Select(
                attrs={
                    'class': 'form-select',
                    'placeholder': 'Venue name*'
                }
            ),
            'attendees': forms.SelectMultiple(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Attendees'
                }
            ),
            'description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Description'
                }
            )
        }
