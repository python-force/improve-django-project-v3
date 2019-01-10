from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import datetime
from .models import Menu, Item
from .forms import MenuForm
from django.utils import timezone


def menu_list(request):
    menus = Menu.objects.all().filter(expiration_date__lte=timezone.now()).order_by('expiration_date')
    return render(request, 'menu/list_all_current_menus.html', {'menus': menus})

def menu_detail(request, pk):
    menu = Menu.objects.get(pk=pk)
    return render(request, 'menu/menu_detail.html', {'menu': menu})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'menu/detail_item.html', {'item': item})

def create_new_menu(request):
    if request.method == "POST":
        form = MenuForm(request.POST)
        if form.is_valid():
            menu = form.save(commit=False)
            menu.created_date = timezone.now()
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm()
    return render(request, 'menu/menu_edit.html', {'form': form})

def edit_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == "POST":
        form = MenuForm(request.POST, instance=menu)
        if form.is_valid():
            menu.season = form.cleaned_data["season"]
            menu.expiration_date = form.cleaned_data['expiration_date']
            menu.items.set(form.cleaned_data['items'])
            menu.save()
            return redirect('menu_detail', pk=menu.pk)
    else:
        form = MenuForm(instance=menu)
    return render(request, 'menu/change_menu.html', {'form':form})


"""
@login_required
def edit_profile(request, profile_slug):
    profile = get_object_or_404(Profile, slug=profile_slug)
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "{} {}'s profile updated."
                             .format(form.cleaned_data["first_name"],
                                     form.cleaned_data["last_name"]))
            return HttpResponseRedirect(profile.get_absolute_url())
    return render(request, "edit-profile.html", {'form': form})
"""
