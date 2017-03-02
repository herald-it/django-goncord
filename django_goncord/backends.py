from django.contrib.auth import logout
from django.contrib.auth import settings
from django.core.exceptions import ImproperlyConfigured

import requests


class Goncord(object):

    login_url = ""
    logout_url = ""
    validate_url = ""
    register_url = ""
    update_payloads_url = ""
    reset_password_url = ""

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

        if 'UPDATE_PAYLOADS_URL' not in settings.GONCORD:
            raise ImproperlyConfigured(
                'Register UPDATE_PAYLOADS_URL in settings.GONCORD required')
        self.update_payloads_url = '%s%s' % (
            settings.GONCORD['BASE_URL'],
            settings.GONCORD['UPDATE_PAYLOADS_URL'])

        if 'RESET_PASSWORD_URL' not in settings.GONCORD:
            raise ImproperlyConfigured(
                'Register RESET_PASSWORD_URL in settings.GONCORD required')
        self.reset_password_url = '%s%s' % (
            settings.GONCORD['BASE_URL'],
            settings.GONCORD['RESET_PASSWORD_URL'])

    def login(self, request, data):
        return requests.post(
            self.login_url, data)

    def logout(self, request):
        logout(request)
        requests.post(self.logout_url, cookies=request.COOKIES)

    def validate(self, request):
        return requests.post(self.validate_url,
                             cookies=request.COOKIES)

    def register(self, data):
        return requests.post(self.register_url, data)

    def update_payload(self, request, data):
        return requests.post(self.update_payloads_url, data,
                             cookies=request.COOKIES)

    def reset_password(self, request, data):
        return requests.post(self.reset_password_url, data,
                             cookies=request.COOKIES)

    def update_user(self, user, data):
        updated = False

        if user.email != data['email']:
            user.email = data['email']
            updated = True

        if 'payload' in data:
            for key, value in data['payload'].items():
                if hasattr(user, key):
                    if getattr(user, key) != data['payload'][key]:
                        setattr(user, key, data['payload'][key])
                        updated = True

        if updated:
            user.save()


goncord = Goncord()
