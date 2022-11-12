from django import forms
from .models import Attendant, EventDetail


class AttendantCreateForm(forms.ModelForm):
    class Meta:
        model = Attendant
        fields = ('day', 'name', 'level', 'phone_number',
                  'visitor', 'department', 'email', 'sex')

    def __init__(self, *args, **kwargs):
        super(AttendantCreateForm, self).__init__(*args, **kwargs)
        self.fields['day'].widget.attrs['placeholder'] = 'day'
        self.fields['day'].help_text = '<small class="text-mute text-danger">select the day of the event</small>'
        self.fields['day'].label = ''

        self.fields['name'].help_text = '<small class="text-mute text-danger">Enter Your Full Name</small>'
        self.fields['name'].widget.attrs['placeholder'] = 'your name'
        self.fields['name'].label = ''


        self.fields['level'].help_text = '<small class="text-mute text-danger">What level are you?</small>'
        self.fields['level'].widget.attrs['placeholder'] = 'level'
        self.fields['level'].label = ''


        self.fields['phone_number'].help_text = '<small class="text-mute text-danger">Enter your Mobile Number: 08103304043</small>'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Your Mobile Number'
        self.fields['phone_number'].label = ''


        self.fields['visitor'].help_text = '<small class="text-mute text-danger">Select if you are visitor from the drop down</small>'
        self.fields['visitor'].label = ''


        self.fields['department'].help_text = '<small class="text-mute text-danger">What department are you?</small>'
        self.fields['department'].widget.attrs['placeholder'] = 'your department'
        self.fields['department'].label = ''


        self.fields['email'].help_text = '<small class="text-mute text-danger">Your Email Address.</small>'
        self.fields['email'].widget.attrs['placeholder'] = 'Your E-mail Address'
        self.fields['email'].label = ''

        self.fields['sex'].help_text = '<small class="text-mute text-danger">Select your Sex Male | Female.</small>'
        self.fields['sex'].label = ''



class EventCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventCreateForm, self).__init__(*args, **kwargs)
        # self.fields['date'].disabled = True
        self.fields['date'].label = ''
        self.fields['date'].help_text = '<small class="text-mute text-danger">The date is generated Automatically (YYYY-MM-DD). </small>'

        self.fields['event_name'].help_text = '<small class="text-mute text-danger">Enter the name of the event...  </small>'
        self.fields['event_name'].widget.attrs['placeholder'] = 'name of the event...'
        self.fields['event_name'].label = ''
    class Meta:
        model = EventDetail
        exclude = ['year', 'slug']
