from django.urls import path
from . import views

app_name = 'manteki'

urlpatterns = [
    path('', views.job_list, name='job_list'),
    path('<int:job_id>/', views.job_detail, name='job_detail'),
   path('<int:job_id>/apply/', views.apply_to_job, name='apply_to_job'),
   path('<int:job_id>/track/', views.track_applications, name='track_applications'),
   path('applications/<int:application_id>/schedule-interview/', views.schedule_interview,name='schedule_interview'),
   path('applications/<int:application_id>/offer-letter/', views.generate_offer_letter, name='generate_offer_letter'),
   path('employee-documents/upload/', views.upload_employee_document, name='upload_employee_document'),
   path('employee-documents/', views.employee_documents, name='employee_documents'),
]