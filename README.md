# django-goncord
Django auth system.

Tested with Django 1.10.4 and Python 3.5.

## Installation guide

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
}
```

You can define your own authentication urls

```python
GONCORD = {
    ...
    'VALIDATE_URL': 'SUB_URL like /validate',
    'LOGIN_URL': 'SUB_URL like /login',
    'LOGOUT_URL': 'SUB_URL like /logout',
    'REGISTER_URL': 'SUB_URL like /register',
    'UPDATE_PAYLOADS_URL': 'SUB_URL like /update',
    'RESET_PASSWORD_URL': 'SUB_URL like /reset_password',
    ...
}
```

at the end specify Django **LOGIN_URL** parameter

for working with package use **login_required** decorator from **django.contrib.auth.decorators**

For using special methods like **login** import **goncord** from **django_goncord.backends**

## django_goncord.backends.goncord methods

### login(request, data)
provide request for authenticate user
> require: django request object and data for submitting to remote server

### logout(request)
provide request for logout user
> require: django request object

### validate(request)
provide token validation for user on remote server
> require: django request object

### register(data)
provide user registration request
> require: data for submitting to remote server

### reset_password(request, data)
provide password reset for authenticated user
> require: django request object and data for submitting to remote server

all methods return response result from remote server
