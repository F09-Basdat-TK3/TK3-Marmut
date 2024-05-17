from django.shortcuts import render
from fitur_biru.queries import *
from datetime import datetime
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import uuid

def show_podcast(request):
    return render(request, "chart-detail.html", {})

def get_podcasts_by_user(request, podcaster_email):
    podster = query(f"SELECT * FROM PODCAST WHERE email = ")
    pod = query(f"SELECT * FROM PODCAST WHERE email_podcaster = '{podcaster_email}'")
    

def get_podcast_by_id(request, id_konten):
    pod = query(f"SELECT * FROM PODCAST WHERE id_konten = '{id_konten}'")
    eps = get_episodes()
    context = {
        'podcast': pod,
        'eps': eps
    }
    return render(request, "podcast.html", context)

def get_episodes(id_konten):
    eps = query("SELECT * FROM episode WHERE id_konten_podcast = '{id_konten}'")
    return eps

def create_podcast(request):
    if request.method == 'POST':
        judul = request.POST.get("judul")
        genre = request.POST.get("genre")
        query(f"INSERT INTO PODCAST VALUE ({judul},{genre})")
        return render(request, "podcast-list.html")
    else: return render(request, "create-podcast.html")

def delete_podcast(request):
    if request.method == 'POST':
        id_konten = request.POST.get("id_konten")
        query(f"DELETE FROM PODCAST WHERE id_konten = '{id_konten}'")
    else: return render(request, "podcast-list.html")

def create_episode(request):
    if request.method == 'POST':
        id_podcast = request.POST.get("id_konten_podcast")
        judul = request.POST.get("judul")
        deskripsi = request.POST.get("deskripsi")
        durasi = request.POST.get("durasi")
        query(f"INSERT INTO EPISODE VALUE ({str(uuid.uuid4())},{id_podcast},{judul},{deskripsi},{durasi},{datetime.now().date()})")
    return render("episode-list.html")

def delete_episode(request):
    if request.method == 'POST':
        id_episode = request.POST.get("id_episode")
        query(f"DELETE FROM EPISODE WHERE id_episode = '{id_episode}'")
    return render("episode-list.html")

def get_chart(request, tipe):
    chart = query(f"SELECT * FROM CHART WHERE tipe = {tipe}")[0]
    id_playlist = chart["id_playlist"]