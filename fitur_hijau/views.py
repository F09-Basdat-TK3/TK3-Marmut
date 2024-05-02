from django.shortcuts import render

def show_no_playlist(request):
    return render(request, "no_playlist.html", {})

def show_user_playlist(request):
    return render(request, "user_playlist.html", {})

def show_create_playlist(request):
    return render(request, "create_playlist.html", {})

def show_detail_playlist(request):
    return render(request, "detail_playlist.html", {})

def show_tambah_lagu(request):
    return render(request, "tambah_lagu.html", {})

def show_detail_song(request):
    return render(request, "detail_song.html", {})

def show_tambah_lagu_ke_playlist(request):
    return render(request, "tambah_lagu_ke_playlist.html", {})

def show_tambah_lagu_ke_playlist_success(request):
    return render(request, "tambah_lagu_ke_playlist_success.html", {})

def show_tambah_download_success(request):
    return render(request, "tambah_download_success.html", {})

def show_detail_playlist_shuffle(request):
    return render(request, "detail_playlist_shuffle.html", {})