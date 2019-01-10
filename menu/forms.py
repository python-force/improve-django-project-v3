from django import forms
#widget=forms.SelectDateWidget
from .models import Menu, Item, Ingredient

class MenuForm(forms.ModelForm):

    class Meta:
        model = Menu
        exclude = ('created_date',)