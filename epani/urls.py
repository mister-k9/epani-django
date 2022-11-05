from django.urls import path

from . import views


urlpatterns = [
    path('', views.epani, name='epani'),
    path('machine/', views.machine, name='machine'),
    path('edit_machine/', views.edit_machine, name='edit_machine'),

    path('clusters/', views.clusters, name='clusters'),
    path('new_cluster/', views.new_cluster, name='new_cluster'),
    path('edit_cluster/', views.edit_cluster, name='edit_cluster'),
    path('cluster/', views.cluster, name='cluster'),

    path('users/', views.users, name='users'),
    path('edit_user/', views.edit_user, name='edit_user'),

    path('cards/', views.cards, name='cards'),
    path('card/', views.card, name='card'),
    path('cards/edit_card/', views.edit_card, name='edit_card'),

    path('orders/', views.orders, name='orders'),
    path('order/', views.order, name='order'),



]
