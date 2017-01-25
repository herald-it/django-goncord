from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.contrib import auth

from .backends import goncord

import base64
import json


class GoncordMiddleware(RemoteUserMiddleware):

    cookie_name = 'jwt'

    def validate(self, request):
        r = goncord.validate(request)

        if r.status_code != 200:
            return

        creds = r.json()
        if creds['payload']:
            creds['payload'] = json.loads(creds['payload'].replace("'", '"'))

        return creds

    def decode_base64(self, data):
        missing_padding = len(data) % 4
        if missing_padding != 0:
            data += '=' * (4 - missing_padding)
        return base64.b64decode(data).decode()

    def process_request(self, request):

        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")

        try:
            token = request.COOKIES[self.cookie_name]
        except KeyError:
            if request.user.is_authenticated:
                self._remove_invalid_user(request)
            return

        if request.user.is_authenticated():
            payloads = token.split('.')[1]
            payloads = json.loads(self.decode_base64(payloads))
            if request.user.get_username() == \
                    self.clean_username(payloads['login'], request):
                return
            else:
                self._remove_invalid_user(request)

        payloads = self.validate(request)
        if payloads is None:
            return

        user = auth.authenticate(remote_user=payloads['login'])
        goncord.update_user(user, payloads)

        if user:
            request.user = user
            auth.login(request, user)
