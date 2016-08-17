from pip.req import parse_requirements
from setuptools import setup, find_packages
import os

DIR = os.path.dirname(os.path.abspath(__file__))

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
    include_package_data = True,
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        str(r.req)
        for r in parse_requirements(DIR + '/requirements.txt', session=False)
    ]
)
