from django import forms
from service_objects.services import Service


class LikeToggleService(Service):
    slug = forms.SlugField()

    custom_validations = []

    def process(self):
        pass
