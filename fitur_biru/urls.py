from django.urls import path
from fitur_biru.views import *

app_name = 'fitur_biru'

urlpatterns = [
    path('', show_podcasters, name='show_podcasters'),
    path('show-podcasts/<str:podcaster_email>', show_podcasts, name="show-podcasts"),
    path('add-podcast/<str:email_podcaster>', add_podcast, name='add-podcast'),
    path('create-podcast/<str:email_podcaster>', create_podcast, name='create-podcast'),
    path('delete-podcast/<str:id_konten>', delete_podcast, name='delete-podcast'),
    path('show-episodes/<str:id_konten>', show_episodes, name='show-episodes'),
    path('add-episode/<str:id_konten>', add_episode, name='add-episode'),
    path('create-episode/<str:id_konten>', create_episode, name='create-episode'),
    path('delete-episode/<str:id_episode>', delete_episode, name='delete-episode'),
    path('charts', show_charts, name='charts'),
    path('chart-content/<str:tipe>', show_chart_content, name='chart-content'),
]