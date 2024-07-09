from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('party/', views.party_room, name='party_room'),
    ]
