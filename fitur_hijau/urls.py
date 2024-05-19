from django.urls import path
from fitur_hijau.views import *

app_name = 'fitur_biru'

urlpatterns = [
    path('create_playlist.html', tambah_playlist, name='create_playlist'),
    path('user_playlist.html', show_playlists, name='user_playlists'),
    path('detail_playlist/<int:id_playlist>/', detail_playlist, name='detail_playlist'),
    path('edit_playlist.html', ubah_playlist, name='edit_playlist'),
    path('delete_playlist.html', delete_playlist, name='delete_playlist'),
    path('add_song.html', tambah_lagu, name='add_song'),
    path('delete_song.html', delete_song, name='delete_song'),
    path('detail_song.html', detail_song, name='detail_song'),
    path('add_song_to_playlist.html', add_song_to_playlist, name='add_song_to_playlist'),
    path('play_song.html', play_song, name='play_song'),

    # path('', show_no_playlist, name='show_no_playlist'),
    # path('create_playlist.html', show_create_playlist, name='show_create_playlist'),
    # path('user_playlist.html', show_user_playlist, name='show_user_playlist'),
    # path('detail_playlist.html', show_detail_playlist, name='show_detail_playlist'),
    # path('detail_playlist_shuffle.html', show_detail_playlist_shuffle, name='show_detail_playlist_shuffle'),
    # path('play_song.html', show_play_song, name='show_play_song'),
    # path('tambah_lagu.html', show_tambah_lagu, name='show_tambah_lagu'),
    # path('detail_song.html', show_detail_song, name='show_detail_song'),
    # path('tambah_lagu_ke_playlist.html', show_tambah_lagu_ke_playlist, name='tambah_lagu_ke_playlist'),
    # path('tambah_lagu_ke_playlist_success.html', show_tambah_lagu_ke_playlist_success, name='show_tambah_lagu_ke_playlist_success'),
    # path('tambah_download_success.html', show_tambah_download_success, name='show_tambah_download_success'),
]
