from . import views
from django.urls import path

urlpatterns = [
    path('', views.service_order_list, name='service_order'),
    path('delete/<int:id>', views.service_order_delete, name='service_order_delete'),
    path('add/', views.service_order_add, name='service_order_add'),
    path('edit/<int:id>', views.service_order_update, name='service_order_update'),
    path('submit/<int:id>', views.service_order_submit, name='service_order_submit'),
    # path('did/', views.did, name='did'),
    # path('did/edit/<int:id>', views.did_edit, name='did_edit'),
    # path('export-csv/', views.export_csv, name='export-csv'),
    # path('export-error-report-csv/', views.export_error_csv, name='export-error-report-csv'),
    # path('register', views.register, name='register'),
    # path('register/success/', views.register_success, name='register_success'),
    # path('user/', views.users, name='user'),
    # path('user/delete/<int:id>', views.user_delete, name='user_delete'),
    # path('user/edit/<int:id>', views.user_edit, name='user_edit'),
    # path('user/update/<int:id>', views.user_update, name='user_update'),
    # path('user/add/', views.user_add, name='user_add'),
    # path('user/create/', views.user_create, name='user_create'),
]
