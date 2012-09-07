#!/usr/bin/env python
import os
import re
from setuptools import setup, find_packages

__doc__="""
Reusable Contact Form application for Django
"""

version = '0.0.1'

setup(name='django-fusionbox-contact',
    version=version,
    description='Reusable Contact Form application for Django',
    author='Fusionbox programmers',
    author_email='programmers@fusionbox.com',
    keywords='django contact',
    long_description=__doc__,
    url='https://github.com/fusionbox/django-fusionbox-contact',
    packages=find_packages(),
    namespace_packages=['fusionbox'],
    platforms = "any",
    license='BSD',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
    ],
    install_requires = ['django_fusionbox'],
    requires = ['django_fusionbox'],
)

