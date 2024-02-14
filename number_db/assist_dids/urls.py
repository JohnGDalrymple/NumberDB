from . import views
from django.urls import path

urlpatterns = [
    path('did_status/', views.did_status, name='did_status'),
    path('did_voice_sms_carrier/', views.did_voice_sms_carrier, name='did_voice_sms_carrier'),
    path('did_sms_type_term_location/', views.did_sms_type_term_location, name='did_sms_type_term_location'),
    path('service_status_add/', views.did_service_status_add, name='did_service_status_add'),
    path('service_status_read/<int:id>', views.did_service_status_read, name='did_service_status_read'),
    path('service_status_update/<int:id>', views.did_service_status_update, name='did_service_status_update'),
    path('service_status_delete/<int:id>', views.did_service_status_delete, name='did_service_status_delete'),
    path('voice_carrier_add/', views.did_voice_carrier_add, name='did_voice_carrier_add'),
    path('voice_carrier_read/<int:id>', views.did_voice_carrier_read, name='did_voice_carrier_read'),
    path('voice_carrier_update/<int:id>', views.did_voice_carrier_update, name='did_voice_carrier_update'),
    path('voice_carrier_delete/<int:id>', views.did_voice_carrier_delete, name='did_voice_carrier_delete'),
    path('sms_carrier_add/', views.did_sms_carrier_add, name='did_sms_carrier_add'),
    path('sms_carrier_read/<int:id>', views.did_sms_carrier_read, name='did_sms_carrier_read'),
    path('sms_carrier_update/<int:id>', views.did_sms_carrier_update, name='did_sms_carrier_update'),
    path('sms_carrier_delete/<int:id>', views.did_sms_carrier_delete, name='did_sms_carrier_delete'),
    path('sms_type_add/', views.did_sms_type_add, name='did_sms_type_add'),
    path('sms_type_read/<int:id>', views.did_sms_type_read, name='did_sms_type_read'),
    path('sms_type_update/<int:id>', views.did_sms_type_update, name='did_sms_type_update'),
    path('sms_type_delete/<int:id>', views.did_sms_type_delete, name='did_sms_type_delete'),
    path('term_location_add/', views.did_term_location_add, name='did_term_location_add'),
    path('term_location_read/<int:id>', views.did_term_location_read, name='did_term_location_read'),
    path('term_location_update/<int:id>', views.did_term_location_update, name='did_term_location_update'),
    path('term_location_delete/<int:id>', views.did_term_location_delete, name='did_term_location_delete'),
]
