from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('<int:pk>/edit/', views.edit_menu, name='menu_edit'),
    path('<int:pk>/', views.menu_detail, name='menu_detail'),
    path('items/<int:pk>/edit', views.edit_item, name='item_edit'),
    path('items/<int:pk>/', views.item_detail, name='item_detail'),
    path('items/', views.item_list, name='item_list'),
    path('new/', views.create_new_menu, name='menu_new'),
]
