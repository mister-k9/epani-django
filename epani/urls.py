from django.urls import path

from . import views


urlpatterns = [
    path('', views.epani, name='epani'),
    path('cards/', views.cards, name='cards'),
    path('orders/', views.orders, name='orders'),
    path('order/', views.order, name='order'),
    path('card/', views.card, name='card'),
    path('machine/', views.machine, name='machine'),
    path('cards/edit_card/', views.edit_card, name='edit_card'),
    
]
