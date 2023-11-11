from django.views.generic import TemplateView
from .models import User


class ProfileView(TemplateView):
    model = User
    template_name = 'users/profile.html'
