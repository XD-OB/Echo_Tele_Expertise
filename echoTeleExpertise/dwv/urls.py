from django.urls import path, include
from . import views

app_name = 'dwv'

urlpatterns = [
    path('', views.dwv_display, name="display"),
]