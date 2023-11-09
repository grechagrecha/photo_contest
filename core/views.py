from django.views import ListView


class HomeView(ListView):
    model = None
    template_name = "home.html"
