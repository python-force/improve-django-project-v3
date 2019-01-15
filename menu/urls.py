from django.urls import path

from . import views

urlpatterns = [
    path('', views.menu_list, name='menu_list'),
    path('<int:pk>/edit/', views.edit_menu, name='menu_edit'),
    path('<int:pk>/', views.menu_detail, name='menu_detail'),
    # path('item/<int:pk>/edit', views.item_detail, name='item_edit'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/', views.item_list, name='item_list'),
    path('new/', views.create_new_menu, name='menu_new'),
]