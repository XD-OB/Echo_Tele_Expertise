from django.urls import path, include
from . import views

app_name = 'accounts'

urlpatterns = [
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('img_profile/', views.upload_profile_img, name="upload_profile_img"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
]