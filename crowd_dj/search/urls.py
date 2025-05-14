from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_song, name='search_song'),
    path('add/', views.add_to_playlist, name='add_to_playlist'),
    path('playlist/', views.view_playlist, name='view_playlist'),
]
