from service_objects.services import ServiceWithResult
from service_objects.fields import ModelField
from rest_framework.authtoken.models import Token

from apps.users.models import User


class TokenGetOrCreateService(ServiceWithResult):
    """
        Returns or creates a Token when given User.
    """
    user = ModelField(User)
    token = None

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.token, created = Token.objects.get_or_create(user=self.cleaned_data['user'])
            self.result = self.token
        return self
