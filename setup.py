#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re

from distribute_setup import use_setuptools; use_setuptools()
from setuptools import setup, find_packages


rel_file = lambda *args: os.path.join(os.path.dirname(os.path.abspath(__file__)), *args)

def read_from(filename):
    fp = open(filename)
    try:
        return fp.read()
    finally:
        fp.close()

def get_version():
    data = read_from(rel_file('src', 'djqmixin', '__init__.py'))
    return re.search(r"__version__ = '([^']+)'", data).group(1)


setup(
    name             = 'django-qmixin',
    version          = get_version(),
    author           = "Zachary Voase",
    author_email     = "zacharyvoase@me.com",
    url              = 'http://bitbucket.org/zacharyvoase/django-qmixin',
    description      = "A Django app for extending managers and the querysets they produce.",
    packages         = find_packages(where='src'),
    package_dir      = {'': 'src'},
)
