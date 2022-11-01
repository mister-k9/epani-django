from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('', views.api_home),
    path('auth/',obtain_auth_token),


    path('cards/', views.CardListCreateAPIView.as_view()),
    path('cards/<str:card_number>/',views.CardDetailAPIView.as_view()),
    path('cards/<str:card_number>/update/',views.CardUpdateAPIView.as_view()),
    path('cards/<str:card_number>/delete/',views.CardDestroyAPIView.as_view()),

    path('orders/', views.OrderListCreateAPIView.as_view()),
    path('orders/<str:order_id>/',views.OrderDetailAPIView.as_view()),
    path('orders/<str:order_id>/update/',views.OrderUpdateAPIView.as_view()),
    path('orders/<str:order_id>/delete/',views.OrderDestroyAPIView.as_view()),

    path('machines/', views.MachineListCreateAPIView.as_view()),
    path('machines/<str:machine_id>/',views.MachineDetailAPIView.as_view()),
    path('machines/<str:machine_id>/update/',views.MachineUpdateAPIView.as_view()),
    path('machines/<str:machine_id>/delete/',views.MachineDestroyAPIView.as_view()),

    path('machine_cards/', views.machine_cards)
]
