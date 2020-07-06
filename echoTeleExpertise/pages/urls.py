from django.urls import path, include
from . import views

app_name = 'pages'

urlpatterns = [
    path('list_patients/', views.list_patients, name="list_patients"),
    path('telefiles/', views.telefiles, name="telefiles"),
    path('telefile/<int:request_id>', views.telefile, name="telefile"),
    path('telefile/share/<int:request_id>', views.share_request, name="share_request"),
    path('telefile/share_request/<int:request_id>', views.share_telefile, name="share_telefile"),
    path('telefile/send/<int:request_id>', views.send_rapport, name="send_rapport"),
    path('list_requests/', views.list_requests, name="list_requests"),
    path('list_doctors/', views.list_doctors, name="list_doctors"),
    path('doctor/<int:doctor_id>', views.doctor, name="doctor"),
    path('requests_history/', views.requests_history, name="requests_history"),
    path('opinions_history/', views.opinions_history, name="opinions_history")
]