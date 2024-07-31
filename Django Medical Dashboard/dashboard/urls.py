from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('appointment/create/', views.create_appointment, name='create_appointment'),
    path('appointment/cancel/<int:appointment_id>/', views.cancel_appointment, name='cancel_appointment'),
    path('message/send/', views.send_message, name='send_message'),
    path('messages/', views.view_messages, name='view_messages'),
    path('medical-records/', views.view_medical_records, name='view_medical_records'),
    path('medical-records/create/<int:patient_id>/', views.create_medical_record, name='create_medical_record'),
    path('notifications/', views.view_notifications, name='view_notifications'),
    path('search/', views.search_patients, name='search_patients'),
    path('login/', auth_views.LoginView.as_view(template_name='dashboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('register/', views.register, name='register'),
    path('survivor/login/', views.survivor_login, name='survivor_login'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),    
]
