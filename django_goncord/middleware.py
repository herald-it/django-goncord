from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured
from django.contrib import auth

from .backends import goncord


class GoncordMiddleware(RemoteUserMiddleware):

    cookie_name = 'jwt'

    def validate(self, request):
        r = goncord.validate(request)

        if not r.ok:
            return None
        return r.json()

    def process_request(self, request):

        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")

        if self.cookie_name not in request.COOKIES:
            if request.user.is_authenticated:
                self._remove_invalid_user(request)
            return

        payloads = self.validate(request)
        if payloads is None:
            if request.user.is_authenticated():
                self._remove_invalid_user(request)
            return

        if request.user.is_authenticated():
            if request.user.get_username() == \
                    self.clean_username(payloads['login'], request):
                goncord.sync_user(request.user, payloads)
                return
            else:
                self._remove_invalid_user(request)

        user = auth.authenticate(remote_user=payloads['login'])
        if user:
            goncord.sync_user(user, payloads)
            auth.login(request, user)
            request.user = user
