from django.urls import path
from fitur_hijau.views import *

app_name = 'fitur_biru'

urlpatterns = [
    path('', show_no_playlist, name='show_no_playlist'),
    path('create_playlist.html', show_create_playlist, name='show_create_playlist'),
    path('user_playlist.html', show_user_playlist, name='show_user_playlist'),
    path('detail_playlist.html', show_detail_playlist, name='show_detail_playlist'),
    path('detail_playlist_shuffle.html', show_detail_playlist, name='show_detail_playlist_shuffle'),
    path('tambah_lagu.html', show_tambah_lagu, name='show_tambah_lagu'),
    path('detail_song.html', show_detail_song, name='show_detail_song'),
    path('tambah_lagu_ke_playlist.html', show_tambah_lagu_ke_playlist, name='tambah_lagu_ke_playlist'),
    path('tambah_lagu_ke_playlist_success.html', show_tambah_lagu_ke_playlist_success, name='show_tambah_lagu_ke_playlist_success'),
    path('tambah_download_success.html', show_tambah_download_success, name='show_tambah_download_success'),
]
