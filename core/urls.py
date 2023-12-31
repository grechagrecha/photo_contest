from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls')),
    path('', views.HomeView.as_view(), name='home'),
    path('add-post/', views.AddPostView.as_view(), name='add-post'),
    path('posts/<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),
    path('post-delete/<slug:slug>', views.PostDeleteView.as_view(), name='post-delete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
