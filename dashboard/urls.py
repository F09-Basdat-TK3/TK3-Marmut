from django.urls import path
from .views import show_dashboard

app_name = 'dashboard'

urlpatterns = [
    path('show_dashboard/', show_dashboard, name='show_dashboard'),
]