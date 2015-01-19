#!/usr/bin/env python
"""
Install django-chainable-manager using setuptools
"""

from setuptools import setup, find_packages

from chainablemanager import __version__

with open('README.rst', 'r') as f:
    readme = f.read()

setup(
    name='django-chainable-manager',
    version=__version__,
    description='Chainable methods on Model managers',
    long_description=readme,
    author='Tim Heap',
    author_email='tim@timheap.me',
    url='https://bitbucket.org/tim_heap/django-chainable-manager',

    install_requires=['Django>=1.4'],
    zip_safe=False,

    packages=find_packages(),

    include_package_data=True,
    package_data={},

    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
)
