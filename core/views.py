from django.views.generic import TemplateView


class HomeView(TemplateView):
    model = None
    template_name = "home.html"
