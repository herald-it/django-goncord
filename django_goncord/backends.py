from django.contrib.auth import logout
from django.contrib.auth import settings
from django.core.exceptions import ImproperlyConfigured

import requests


class Goncord(object):

    login_url = ""
    logout_url = ""
    validate_url = ""
    register_url = ""

    def __init__(self):
        if not hasattr(settings, 'GONCORD'):
            raise ImproperlyConfigured('Register GONCORD in settings required')

        if 'BASE_URL' not in settings.GONCORD:
            raise ImproperlyConfigured(
                'Register BASE_URL in settings.GONCORD required')

        if 'LOGIN_URL' not in settings.GONCORD:
            raise ImproperlyConfigured(
                'Register LOGIN_URL in settings.GONCORD required')
        self.login_url = '%s%s' % (
            settings.GONCORD['BASE_URL'], settings.GONCORD['LOGIN_URL'])

        if 'LOGOUT_URL' not in settings.GONCORD:
            raise ImproperlyConfigured(
                'Register LOGOUT_URL in settings.GONCORD required')
        self.logout_url = '%s%s' % (
            settings.GONCORD['BASE_URL'], settings.GONCORD['LOGOUT_URL'])

        if 'VALIDATE_URL' not in settings.GONCORD:
            raise ImproperlyConfigured(
                'Register VALIDATE_URL in settings.GONCORD required')
        self.validate_url = '%s%s' % (
            settings.GONCORD['BASE_URL'], settings.GONCORD['VALIDATE_URL'])

        if 'REGISTER_URL' not in settings.GONCORD:
            raise ImproperlyConfigured(
                'Register REGISTER_URL in settings.GONCORD required')
        self.register_url = '%s%s' % (
            settings.GONCORD['BASE_URL'], settings.GONCORD['REGISTER_URL'])

    def login(self, request, data):
        return requests.post(
            self.login_url, data)

    def logout(self, request):
        logout(request)
        requests.post(self.logout_url, cookies=request.COOKIES)

    def validate(self, request):
        return requests.post(self.validate_url,
                             cookies=request.COOKIES)

    def register(self, request, data):
        return requests.post(self.register_url, data)

    def update_user(self, user, data):
        user.first_name = data['payload']['first_name']
        user.last_name = data['payload']['last_name']
        user.email = data['email']
        user.save()


goncord = Goncord()
