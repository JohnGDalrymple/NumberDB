from . import views
from django.urls import path

urlpatterns = [
    path('did_status_type/', views.did_status_type, name='did_status_type'),
    path('did_voice_sms_carrier/', views.did_voice_sms_carrier, name='did_voice_sms_carrier'),
    path('did_sms_type_term_location/', views.did_sms_type_term_location, name='did_sms_type_term_location'),
    path('service_type_add/', views.did_serivce_type_add, name='did_serivce_type_add'),
    path('service_status_add/', views.did_serivce_status_add, name='did_serivce_status_add'),
    path('service_status_read/<int:id>', views.did_service_status_read, name='service_status_read'),
    path('service_status_update/<int:id>', views.did_service_status_update, name='service_status_update'),
    path('service_status_delete/<int:id>', views.did_service_status_delete, name='service_status_delete'),
]
