

class ValidationMixin:
    result = None
    custom_validations = []

    def run_custom_validations(self):
        for validation in self.custom_validations:
            getattr(self, validation)()
