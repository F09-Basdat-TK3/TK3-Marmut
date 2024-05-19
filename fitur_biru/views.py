from django.shortcuts import render
from fitur_biru.queries import *
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import uuid

def show_podcasters(request):
    podster = query("SELECT A.nama, A.email FROM AKUN A JOIN PODCASTER PR ON A.email = PR.email")
    context = {'podcasters': podster}
    return render(request, "podcaster-list.html", context)

def show_podcasts(request, podcaster_email):
    pods = query(f"""
                  SELECT K.judul, K.durasi, P.id_konten, COUNT(E.id_episode) AS jumlah_episode
                  FROM KONTEN K
                  JOIN PODCAST P ON K.id = P.id_konten
                  JOIN EPISODE E ON P.id_konten = E.id_konten_podcast
                  WHERE P.email_podcaster = '{podcaster_email}'
                  GROUP BY K.judul, K.durasi, P.id_konten
                  """)
    context = {'podcasts': pods, 'podster_email': podcaster_email}
    return render(request, "podcast-list-podcaster.html", context)

def show_episodes(request, id_konten):
    pod_title = query(f"""
                       SELECT K.judul FROM KONTEN K
                       JOIN PODCAST P ON K.id = P.id_konten
                       WHERE P.id_konten = '{id_konten}'
                       """)[0]["judul"]
    eps = query(f"SELECT * FROM EPISODE WHERE id_konten_podcast = '{id_konten}'")
    context = {'pod_title': pod_title, 'eps': eps}
    return render(request, "episode-list-podcaster.html", context)

def add_podcast(request, email_podcaster):
    genre = query(f"SELECT DISTINCT genre FROM GENRE")
    context = {'podster_email': email_podcaster, 'genres': genre}
    return render(request, "create-podcast.html", context)

@csrf_exempt
def create_podcast(request, email_podcaster):
    if request.method == 'POST':
        judul = request.POST.get("title")
        genres = request.POST.getlist("multval")
        id = str(uuid.uuid4())
        query(f"INSERT INTO KONTEN VALUES ('{id}','{judul}','{datetime.now().date()}','{datetime.now().year}','0')")
        query(f"INSERT INTO PODCAST VALUES ('{id}','{email_podcaster}')")
        for g in genres:
            query(f"INSERT INTO GENRE VALUES ('{id}','{g}')")
    return show_podcasts(request, email_podcaster)

def delete_podcast(request, id_konten):
    podster_email = get_podster_email_by_id_konten(id_konten)
    query(f"DELETE FROM PODCAST WHERE id_konten = '{id_konten}'")
    return show_podcasts(request, podster_email)

def add_episode(request, id_konten):
    context = {'id_konten': id_konten}
    return render(request, "create-episode.html", context)

@csrf_exempt
def create_episode(request, id_konten):
    if request.method == 'POST':
        judul = request.POST.get("title")
        deskripsi = request.POST.get("description")
        durasi = request.POST.get("duration")
        query(f"INSERT INTO EPISODE VALUES ('{str(uuid.uuid4())}','{id_konten}','{judul}','{deskripsi}','{durasi}','{datetime.now().date()}')")
        return HttpResponseRedirect(reverse('fitur_biru:show-episodes', args=[id_konten]))
    return render("fitur_biru:podcast-list-podcaster.html")

def delete_episode(request, id_episode):
    id_konten = query(f"SELECT id_konten_podcast FROM EPISODE WHERE id_episode = '{id_episode}'")[0]["id_konten_podcast"]
    query(f"DELETE FROM EPISODE WHERE id_episode = '{id_episode}'")
    return show_episodes(request, id_konten)

def show_charts(request):
    return render(request, "chart-list.html", {})

def show_chart_content(request, tipe):
    songs = query(f"""
                   SELECT KONTEN.judul, AKUN.nama, KONTEN.tanggal_rilis, SONG.total_play
                   FROM CHART
                   JOIN PLAYLIST_SONG ON CHART.id_playlist = PLAYLIST_SONG.id_playlist
                   JOIN SONG ON PLAYLIST_SONG.id_song = SONG.id_konten
                   JOIN ARTIST ON SONG.id_artist = ARTIST.id
                   JOIN AKUN ON ARTIST.email_akun = AKUN.email
                   JOIN KONTEN ON SONG.id_konten = KONTEN.id
                   WHERE CHART.tipe = '{tipe} Top 20'
                   """)
    if tipe == "Daily": range = "Hari"
    elif tipe == "Weekly": range = "Minggu"
    elif tipe == "Monthly": range = "Bulan"
    else: range = "Tahun"
    context = {'tipe': range, 'songs': songs}
    return render(request, "chart-content.html", context)

def get_podster_email_by_id_konten(id_konten):
    return query(f"SELECT email_podcaster FROM PODCAST WHERE id_konten = '{id_konten}'")[0]["email_podcaster"]