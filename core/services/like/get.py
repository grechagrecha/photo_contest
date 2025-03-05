from service_objects.fields import ModelField
from service_objects.services import ServiceWithResult

from apps.users.models import User


class LikeGetFromUserService(ServiceWithResult):
    """
        Service that gets a user and returns bool if user liked that post.
    """
    user = ModelField(User)

    custom_validations = []

    def process(self):
        self.run_custom_validations()
        if self.is_valid():
            self.result = self.cleaned_data['user'].like_set.select_related('post').all()
        return self
