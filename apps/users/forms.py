from allauth.socialaccount.forms import SignupForm


class CustomSocialSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        print(self.sociallogin)
        print(user)

        return user
