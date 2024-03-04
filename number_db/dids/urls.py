from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('did/', views.did, name='did'),
    path('did/sync_method/', views.did_sync_method, name='did_sync_method'),
    path('did/download_all/', views.did_download_all, name='did_download_all'),
    path('did/add/', views.did_add, name='did_add'),
    path('did/delete/<int:id>', views.did_delete, name='did_delete'),
    path('did/edit/<int:id>', views.did_edit, name='did_edit'),
    path('did/update/<int:id>', views.did_update, name='did_update'),
    path('export-csv/', views.export_csv, name='export-csv'),
    path('export-error-report-csv/', views.export_error_csv, name='export-error-report-csv'),
    path('user/', views.users, name='user'),
    path('user/delete/<int:id>', views.user_delete, name='user_delete'),
    path('user/edit/<int:id>', views.user_edit, name='user_edit'),
    path('user/update/<int:id>', views.user_update, name='user_update'),
    path('user/add/', views.user_add, name='user_add'),
    path('user/create/', views.user_add, name='user_create'),
    path('user/verify/', views.user_verify, name='user_verify'),
    path('reset/password/', views.reset_password, name='reset_password'),
    path('did_standardization/', views.did_standardization, name='did_standardization'),
    path('did_standardization/delete/<int:id>', views.did_standardization_delete, name='did_standardization_delete'),
    path('did_standardization/edit/<int:id>', views.did_standardization_edit, name='did_standardization_edit'),
    # path('register', views.register, name='register'),
    # path('register/success/', views.register_success, name='register_success'),
]
