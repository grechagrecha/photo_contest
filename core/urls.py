from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

app_name = 'core'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('apps.users.urls')),
    path('', views.HomeView.as_view(), name='home'),

    path('post/<slug:post_slug>', views.PostDetailView.as_view(), name='post-detail'),
    path('post-create/', views.PostCreateView.as_view(), name='post-create'),
    path('post-delete/<slug:post_slug>', views.PostDeleteView.as_view(), name='post-delete'),
    path('post-update/<slug:post_slug>', views.PostUpdateView.as_view(), name='post-update'),
    path('post-recover/<slug:post_slug>', views.PostRecoverView.as_view(), name='post-recover'),

    path('ajax-search/', views.PostSearchAjaxView.as_view(), name='ajax-search'),

    path('post-like/<slug:slug>', views.PostLikeAjaxView.as_view(), name='post-like'),

    path('comment-create/<slug:post_slug>', views.CommentCreateView.as_view(), name='comment-create'),
    path('comment-update/<slug:comment_slug>', views.CommentUpdateView.as_view(), name='comment-update'),
    path('comment-delete/<slug:comment_slug>', views.CommentDeleteView.as_view(), name='comment-delete'),
    path('comment-reply/<slug:comment_slug>', views.CommentReplyView.as_view(), name='comment-reply'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += (path('__debug__/', include('debug_toolbar.urls')),)
