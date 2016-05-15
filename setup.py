# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='event_client',
    version='0.0.1',
    description='Client for "event storage"."',
    long_description=readme,
    author='Jan Karásek',
    author_email='xkarase1@fi.muni.cz',
    url='',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
