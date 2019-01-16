from django.utils import timezone
from django import forms
from django.forms import ValidationError
from bootstrap_datepicker_plus import DatePickerInput
from .models import Menu, Item


class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['season', 'items', 'expiration_date']
        widgets = {
            'expiration_date': DatePickerInput(),
        }

    def clean_season(self):
        season = self.cleaned_data['season']
        if len(season) < 7:
            raise ValidationError('Please create menu with '
                                  'at least 12 characters.')

        return season

    def clean_expiration_date(self):
        expiration_date = self.cleaned_data['expiration_date']
        if expiration_date < timezone.now():
            raise ValidationError('Select the date in the future.')

        return expiration_date


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'description', 'standard', 'ingredients']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 7:
            raise ValidationError('Please create name with '
                                  'at least 12 characters.')

        return name

    def clean_description(self):
        description = self.cleaned_data['description']
        if len(description) < 25:
            raise ValidationError('Please create description '
                                  'with at least 25 characters.')

        return description
