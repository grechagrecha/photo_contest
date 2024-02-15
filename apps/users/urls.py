from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/on-validation/', views.PostsOnValidationView.as_view(), name='on-validation'),
    path('profile/on-deletion/', views.PostsOnDeletionView.as_view(), name='on-deletion')

]
