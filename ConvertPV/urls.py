"""ConvertPV URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.urls import re_path as url
from django.views.static import serve

from django.contrib.auth import views as auth_views

admin.site.site_header = "ConvertPV"
admin.site.site_title = "ConvertPV Portal"
admin.site.index_title = "Welcome to ConvertPV Portal"

urlpatterns = [
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    path('admin/', admin.site.urls),
    path('convert/', include('convertpvs.urls')),
    path('', auth_views.LoginView.as_view(
        template_name='admin/login.html',
        extra_context={
            # option 1: provide full path
            'next': '/convert/',
            # 'next': '/convert/demo2_r3_converted.xml/r3/'

            # option 2: just provide the name of the url
            # 'next': 'custom_url_name',
        }
    ), name='login'),
]