from . import views
from django.urls import path

urlpatterns = [
    path('', views.customer_list, name='customer'),
    path('delete/<int:id>', views.customer_delete, name='customer_delete'),
    path('add/', views.customer_add, name='customer_add'),
    # path('create/', views.customer_create, name='customer_create'),
    path('edit/<int:id>', views.customer_edit, name='customer_edit'),
    path('update/<int:id>', views.customer_update, name='customer_update'),
    # path('list/', views.list, name='list'),
    path('export-csv/', views.export_csv, name='customer_export_csv'),
    # path('register', views.register, name='register'),
    # path('register/success/', views.register_success, name='register_success'),
    # path('users/', views.users, name='users'),
    # path('users/create/', views.user_create, name='user_create'),
]
