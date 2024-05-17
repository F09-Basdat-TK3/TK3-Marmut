from django.shortcuts import render

def create_album(request):
    return render(request, 'create_album.html')
def list_album(request):
    return render(request, 'list_album.html')
def create_song(request):
    return render(request, 'create_song.html')
def list_songs_in_album(request):
    return render(request, 'list_songs_in_album.html')
def cek_royalty(request):
    return render(request, 'cek_royalty.html')
def create_podcast(request):
    return render(request, 'create_podcast.html')
def list_podcast(request):
    return render(request, 'list_podcast.html')
def create_episode(request):
    return render(request, 'create_episode.html')
def list_episodes_in_podcast(request):
    return render(request, 'list_episodes_in_podcast.html')
def list_album_label(request):
    return render(request, 'list_album_label.html')
def list_songs_in_album_label(request):
    return render(request, 'list_songs_in_album_label.html')
