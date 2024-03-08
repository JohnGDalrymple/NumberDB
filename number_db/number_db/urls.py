"""
URL configuration for number_db project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from django.shortcuts import render


def handler404(request, exception):
    if str(request.user).is_authenticated:
        print('True')
        return render(request, '404.html')
    else:
        print('Fail')
        return render(request, '1404.html')

urlpatterns = [
  path('', include('dids.urls')),
  path('customer/', include('customers.urls')),
  path('assist_did/', include('assist_dids.urls')),
  path('service_order/', include('service_orders.urls')),
  path('admin/', admin.site.urls),
  path('', TemplateView.as_view(template_name='home.html'), name='home'),
  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
  path('logout/', auth_views.LogoutView.as_view(template_name='logged_out.html'), name='logout'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = handler404

