#!/usr/bin/env python
"""
Install django-chainable-manager using setuptools
"""

try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='django-chainable-manager',
    version="0.4.0",
    description='Chainable methods on Model managers',
    author='Tim Heap',
    author_email='heap.tim@gmail.com',
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
