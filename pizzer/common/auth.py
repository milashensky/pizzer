from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from common.mixins import SerializedView


class LoginApi(SerializedView):

    def post(self, request):
        if self.request.user.is_authenticated:
            return {'state': True}
        user = User.objects.filter(email=self.data.get('email')).first()
        if user and user.check_password(self.data.get('password')):
            login(self.request, user)
            return {'state': True}
        return {'errors': ['Incorrect email or password']}


class LogoutApi(SerializedView):

    def post(self, request):
        logout(self.request)
        return {'state': True}


class RegistrationApi(SerializedView):

    def post(self, request):
        form = UserCreationForm(self.data)
        if form.is_valid():
            user = form.save()
            user.email = self.data.get('email')
            user.save()
            login(self.request, user)
            return {'id': user.id}
        return {'errors': form.errors}
