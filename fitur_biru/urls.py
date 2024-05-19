from django.urls import path
from fitur_biru.views import *

app_name = 'fitur_biru'

urlpatterns = [
    path('', show_podcaster, name='show_podcaster'),
    path('show-podcasts/<str:podcaster_email>', show_podcasts, name="show-podcasts"),
    path('show-episodes/<str:id_konten>', show_episodes, name='show-episodes'),
]