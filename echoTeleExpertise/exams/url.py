from django.urls import path, include
from . import views

app_name = 'exams'

urlpatterns = [
    path('add/', views.add_request, name="add_request"),
    path('solved/<int:req_id>', views.request_solved_detail, name="request_solved_detail"),
    path('done/<int:req_id>', views.opinion_solved_detail, name="opinion_solved_detail"),
    path('incomplete/<int:request_id>', views.mark_incomplete, name="mark_incomplete"),
    path('patient/<int:patient_id>', views.patient_request, name="patient_request"),
    path('detail/<int:request_id>', views.request_detail, name="request_detail"),
    path('ask/<int:expert_id>', views.ask_request, name="ask_request"),
    path('request_pdf/<int:request_id>', views.get_request_pdf, name="get_request_pdf"),
    path('opinion_pdf/<int:request_id>', views.get_opinion_pdf, name="get_opinion_pdf")
]