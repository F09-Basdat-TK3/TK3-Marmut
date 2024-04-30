from django.urls import path
from fitur_biru.views import *

app_name = 'fitur_biru'

urlpatterns = [
    path('', show_podcast, name='show_podcast'),
]