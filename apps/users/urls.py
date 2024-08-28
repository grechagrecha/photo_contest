from django.urls import path, include
from . import views

app_name = 'users'

urlpatterns = [
    path('your_posts/', views.YourPostsView.as_view(), name='your-posts'),
    path('profile/<int:pk>', views.ProfileView.as_view(), name='profile'),
    path('login/', views.LoginView.as_view(), name='login')

]
