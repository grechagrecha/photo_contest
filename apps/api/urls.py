from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('get_token/', views.CustomAuthToken.as_view(), name='get-token')
]
