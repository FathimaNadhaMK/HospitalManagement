from django import forms
from .models import Reminder

class ReminderForm(forms.ModelForm):
    class Meta:
        model=Reminder
        fields = ['pt_name','title','description','remind_at']
        widgets={
            'reminded_at' : forms.DateTimeInput(attrs={'type':'datetime-local'})
        }