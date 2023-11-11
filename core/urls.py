from django.contrib import admin
from django.urls import path, include
from . import views
import allauth

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls'))
]
