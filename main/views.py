from django.shortcuts import render

def show_main(request):
    return render(request, "front-page.html", {})