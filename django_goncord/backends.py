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

    x_app_token = ""

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

        if 'UPDATE_USER_URL' not in settings.GONCORD:
            self.update_user_url = '/update'
        else:
            self.update_user_url = '%s%s' % (
                settings.GONCORD['BASE_URL'], settings.GONCORD['UPDATE_USER_URL'])

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

        if hasattr(settings, 'GONCORD_SERVICE_TOKEN'):
            self.x_app_token = settings.GONCORD_SERVICE_TOKEN

    def prepare_cookie(self, request):
        return 'Bearer {}'.format(request.COOKIES['jwt'])

    def login(self, request, data):
        return requests.post(self.login_url, json=data)

    def logout(self, request):
        logout(request)
        return requests.delete(self.logout_url, headers={
            'Authorization': self.prepare_cookie(request)
        })

    def validate(self, request):
        return requests.get(self.validate_url, headers={
            'Authorization': self.prepare_cookie(request)
        })

    def register(self, data):
        return requests.post(self.register_url, json=data)

    def update_user(self, request, data):
        return requests.patch(self.update_user_url, json=data, headers={
            'Authorization': self.prepare_cookie(request),
            'x-app-token': self.x_app_token
        })

    def update_payload(self, request, data):
        return requests.patch(self.update_payloads_url, json=data, headers={
            'Authorization': self.prepare_cookie(request),
            'x-app-token': self.x_app_token
        })

    def reset_password(self, request, data):
        return requests.post(self.reset_password_url, json=data, headers={
            'Authorization': self.prepare_cookie(request)
        })

    def get_menu(self, request):
        r = requests.get(
            '{}{}'.format(settings.GONCORD['BASE_URL'], '/api/v0/menu'),
            headers={
                'Authorization': self.prepare_cookie(request)
            })

        print(r.json())

        if not r.ok:
            return

        return r.json()

    def sync_user(self, user, data):
        updated = False

        for key, value in data.items():
            if hasattr(user, key):
                if getattr(user, key) != data[key]:
                    setattr(user, key, data[key])
                    updated = True

        if updated:
            user.save()


goncord = Goncord()
