from django.contrib.auth.backends import ModelBackend


class UserModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwars):
        """
        @username is email
        @password is password (hash)
        """
        from django.contrib.auth.models import User
        try:
            user = User.objects.get(email=username)
            if user and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        from django.contrib.auth.models import User

        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def backend_authenticate(user):
    user.backend = "%s.%s" % (UserModelBackend.__module__,
                              UserModelBackend.__name__)
