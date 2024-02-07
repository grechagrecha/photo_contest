import hashlib

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import TemplateView

from .models import User


class LoginView(DjangoLoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        return reverse('home')

    def form_invalid(self, form):
        print('Login form is invalid')
        return super().form_invalid(form)

    def form_valid(self, form):
        """
            TODO: Create a separate backend and take all this shit there
        """

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            token = self._generate_token(username, password)
            user.token = token
            user.save()

            self.request.META['HTTP_AUTHORIZATION'] = token
            return super().form_valid(form)

        messages.error(self.request, 'Login failure! Check if the credentials are valid.')
        return HttpResponseRedirect(reverse('users:login'))

    def _generate_token(self, username, password):
        s = username + password + settings.SECRET_KEY
        s = s.encode('utf-8')
        token = hashlib.sha256(s).hexdigest()
        return token


class ProfileView(TemplateView):
    model = User
    template_name = 'users/profile.html'
