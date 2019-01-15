from django import forms
from bootstrap_datepicker_plus import DatePickerInput
from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        fields = ['season', 'items', 'expiration_date']
        widgets = {
            'expiration_date': DatePickerInput(),  # default date-format %m/%d/%Y will be used
        }

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['name', 'description', 'standard', 'ingredients']