from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login')

]
