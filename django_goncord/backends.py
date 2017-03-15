from django.contrib.auth import logout
from django.contrib.auth import settings
from django.core.exceptions import ImproperlyConfigured

import requests
import json


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
            self.login_url = '/login'
        else:
            self.login_url = '%s%s' % (
                settings.GONCORD['BASE_URL'], settings.GONCORD['LOGIN_URL'])

        if 'LOGOUT_URL' not in settings.GONCORD:
            self.logout_url = '/logout'
        else:
            self.logout_url = '%s%s' % (
                settings.GONCORD['BASE_URL'], settings.GONCORD['LOGOUT_URL'])

        if 'VALIDATE_URL' not in settings.GONCORD:
            self.validate_url = '/validate'
        else:
            self.validate_url = '%s%s' % (
                settings.GONCORD['BASE_URL'], settings.GONCORD['VALIDATE_URL'])

        if 'REGISTER_URL' not in settings.GONCORD:
            self.register_url = '/register'
        else:
            self.register_url = '%s%s' % (
                settings.GONCORD['BASE_URL'], settings.GONCORD['REGISTER_URL'])

        if 'UPDATE_PAYLOADS_URL' not in settings.GONCORD:
            self.update_payloads_url = '/update'
        else:
            self.update_payloads_url = '%s%s' % (
                settings.GONCORD['BASE_URL'],
                settings.GONCORD['UPDATE_PAYLOADS_URL'])

        if 'RESET_PASSWORD_URL' not in settings.GONCORD:
            self.reset_password_url = '/reset'
        else:
            self.reset_password_url = '%s%s' % (
                settings.GONCORD['BASE_URL'],
                settings.GONCORD['RESET_PASSWORD_URL'])

    def login(self, request, data):
        return requests.post(self.login_url, data)

    def logout(self, request):
        logout(request)
        requests.post(self.logout_url, cookies=request.COOKIES)

    def validate(self, request):
        return requests.post(self.validate_url, cookies=request.COOKIES)

    def register(self, data):
        return requests.post(self.register_url, data)

    def update_payload(self, request, data):
        return requests.post(self.update_payloads_url, data,
                             cookies=request.COOKIES)

    def reset_password(self, request, data):
        return requests.post(self.reset_password_url, data,
                             cookies=request.COOKIES)

    def get_menu(self, request):
        r = self.validate(request)

        if r.status_code != 200:
            return

        menu = r.json()
        if 'payload' not in menu:
            return {}

        menu = json.loads(menu['payload'].replace("'", '"'))
        if 'roles' not in menu:
            return {}

        return menu['roles']

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
