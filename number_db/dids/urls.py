from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('list', views.list, name='list'),
    path('export-csv/', views.export_csv, name='export-csv'),
    # path('edit/<int:id>', views.edit, name='edit'),
    # path('edit/update/<int:id>', views.update, name='update'),
    # path('delete/<int:id>', views.delete, name='delete'),
    path('register', views.register, name='register'),
    path('register/success/', views.register_success, name='register_success'),
    path('users/', views.users, name='users'),
    path('users/delete/<int:id>', views.user_delete, name='user_delete'),
    path('users/edit/<int:id>', views.user_edit, name='user_edit'),
    path('users/update/<int:id>', views.user_update, name='user_update'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/create/', views.user_create, name='user_create'),
    # path('upload/csv/', views.list, name='upload_csv'),
    # path('change_password', views.changePassword, name='changePassword'),
    # path('file/delete', views.changePassword, name='changePassword'),
    # path('file/delete/<int:id>', views.deleteFiles, name='deleteFiles'),
]
