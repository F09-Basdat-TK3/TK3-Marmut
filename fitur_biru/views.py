from django.shortcuts import render

def show_podcast(request):
    return render(request, "chart-detail.html", {})