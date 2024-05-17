from django.urls import path
from fitur_pink import views
from fitur_pink.views import *

app_name = 'fitur_pink'

urlpatterns = [

    path('create_album/', views.create_album, name='create_album'),
    path('list_album/', views.list_album, name='list_album'),
    path('create_song/', views.create_song, name='create_song'),
    path('list_songs_in_album/', views.list_songs_in_album, name='list_songs_in_album'),
    path('cek_royalty/', views.cek_royalty, name='cek_royalty'),
    path('create_podcast/', views.create_podcast, name='create_podcast'),
    path('list_podcast/', views.list_podcast, name='list_podcast'),
    path('create_episode/', views.create_episode, name='create_episode'),
    path('list_episodes_in_podcast/', views.list_episodes_in_podcast, name='list_episodes_in_podcast'),
    path('list_album_label/', views.list_album_label, name='list_album_label'),
    path('list_songs_in_album_label/', views.list_songs_in_album_label, name='list_songs_in_album_label'),
]
