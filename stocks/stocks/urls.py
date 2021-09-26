"""stocks URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path,include
import user.views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',user_views.home,name="home1"),
    path('download_video',user_views.get_video,name="download_video"),
    path('download_audio',user_views.get_audio,name="download_audio"),
    path('download/<str:client>/<str:fl_path1>',user_views.download,name="download"),
    path("login",auth_views.LoginView.as_view(template_name="user/login.html"),name="login"),
    path('register',user_views.Register,name="register"),
    path('logout',auth_views.LogoutView.as_view(template_name="user/logout.html"),name="logout"),
    path('history',user_views.get_history,name="delete"),
    path('delete_acc/<str:name>',user_views.delete_acc,name="delete_acc"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
