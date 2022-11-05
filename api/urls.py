from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views


urlpatterns = [
    path('deduct_card_balance/', views.deduct_card_balance),
    path('get_cards/', views.get_cards)
]
