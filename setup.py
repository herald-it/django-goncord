import os
import sys
from setuptools import (
    setup,
    find_packages)

version = '0.1.5'

if sys.argv[-1] == 'tag':
    print("Tagging the version on github:")
    os.system("git tag -a %s -m 'version %s'" % (version, version))
    os.system("git push --tags")
    sys.exit()

setup(
    name='django-goncord',
    version=version,
    author='herald-it',
    author_email='scroll42ru@gmail.com',
    maintainer='Dmitry Kuznetsov',
    maintainer_email='scroll42ru@gmail.com',

    url='https://github.com/herald-it/django-goncord',
    download_url='https://github.com/herald-it/django-goncord/archive/%s.tar.gz' % (
        version),

    description='A django widget which allows you to create multiple auth system.',
    long_description=open(os.path.join(
        os.path.dirname(__file__), 'README.md')).read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    license='MIT',

    packages=['django_goncord'],
    include_package_data=True,
    package_data={'': ['*.*']},
    install_requires=['setuptools', 'requests', 'Django>=1.10,<1.11'],
    zip_safe=False,
    keywords=['django', 'auth', 'goncord', 'admin']
)
