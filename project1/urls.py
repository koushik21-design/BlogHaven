"""
URL configuration for project1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from blog import views as BlogsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home,name='home'),
    path('category/',include('blog.urls')),
    path('blogs/search/',BlogsView.search,name='search'),
    path('blogs/<slug:slug>/',BlogsView.blogs,name='blogs'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('dashboard/',include('dashboards.urls')),
    path('blog/<slug:slug>/like/', BlogsView.like_post, name='like_post'),
    path('blog/<slug:slug>/dislike/', BlogsView.dislike_post, name='dislike_post'),
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
