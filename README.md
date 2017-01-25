# django-goncord
Django auth system.

Tested with Django 1.10.4 and Python 3.5.

### Installation guide

First install package using pip

```sh
pip install django-goncord
```

After installation register middleware and authentication backend in settings

```python
MIDDLEWARE_CLASSES = [
    ...
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_goncord.middleware.GoncordMiddleware',
    ...
]

...

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
]
```

Then register auth system url parameters in settings

```python
GONCORD = {
    'BASE_URL': 'URL like http://www.my-site.ru',
    'VALIDATE_URL': 'SUB_URL like /validate',
    'LOGIN_URL': 'SUB_URL like /login',
    'LOGOUT_URL': 'SUB_URL like /logout',
    'REGISTER_URL': 'SUB_URL like /register'
}
```

for authentication you can register only **BASE_URL**, **VALIDATE_URL**, **LOGIN_URL** and **LOGOUT_URL**

at the end specify Django **LOGIN_URL** parameter

for working with package use **login_required** decorator from **django.contrib.auth.decorators**
