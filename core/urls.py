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
    path('post/<slug:slug>', views.PostDetailView.as_view(), name='post-detail'),
    path('post-add/', views.PostAddView.as_view(), name='add-post'),
    path('post-delete/<slug:slug>', views.PostDeleteView.as_view(), name='post-delete'),
    path('post-update/<slug:slug>', views.PostUpdateView.as_view(), name='post-update'),
    path('like/<slug:slug>', views.PostLikeView.as_view(), name='post-like'),
    path('comment-add/<slug:slug>', views.CommentAddView.as_view(), name='add-comment'),
    path('comment-update/<slug:slug>', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment-delete/<int:pk>', views.CommentDeleteView.as_view(), name='delete-comment')

]

# Only for debug mode!
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
