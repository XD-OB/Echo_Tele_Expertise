from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('news/', views.news, name="news"),
    path('admin/', admin.site.urls),
    path('requests/', include('exams.url', namespace="exams")),
    path('accounts/', include('accounts.urls', namespace="accounts")),
    path('patients/', include('patients.urls', namespace="patients")),
    path('pages/', include('pages.urls', namespace="pages")),
    path('dwv/', include('dwv.urls', namespace="dwv")),
    path('verify_email/<str:hash_code>/', views.activate_account, name="activate_account"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)