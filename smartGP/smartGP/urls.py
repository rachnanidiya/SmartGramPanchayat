"""
URL configuration for smartGP project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from main_app import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home,name='home'),
    path('apply/', views.apply,name='apply'),
    path('schemes/', views.schemes,name='schemes'),
    path('login/', views.user_login,name='login'),
    path('register/', views.register,name='register'),
    path('logout/',views.logout_user,name="logout"),
    path('about/',views.about,name='about'),
    path('digital-literacy/',views.digital_literacy,name='digital-literacy'),
    path('healthcare/',views.healthcare,name='healthcare'),
    path('employment/',views.employment,name='employment'),
    path('women/',views.women,name='women'),
    path('energy/',views.energy,name='energy'),
    path('agriculture/',views.agriculture,name='agriculture'),
    path('complaint/',views.complaint,name='complaint'),
    path('ty/',views.thanks,name='thanks'),
    path('success/',views.success,name='success'),
    path('news/', views.news_list, name='news_list'),
    path('profile/', views.user_profile, name='user_profile'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/complaint/approve/<int:complaint_id>/', views.approve_complaint, name='approve_complaint'),
    path('admin-dashboard/scheme/approve/<int:scheme_id>/', views.approve_scheme, name='approve_scheme'),
    path('admin-dashboard/news/edit/<int:news_id>/', views.edit_news, name='edit_news'),
    path('admin-dashboard/news/delete/<int:news_id>/', views.delete_news, name='delete_news'),
    path('admin-dashboard/complaint/delete/<int:complaint_id>/', views.delete_complaint, name='delete_complaint'),
    path('add-news/', views.add_news, name='add_news'),


]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)