import os
from setuptools import setup, find_packages

long_description = file('README.md','r').read()

setup(
    name='vimeo-wrapper',
    version='0.4.3',
    description='A thin wrapper around requests for vimeo',
    long_description=long_description,
    author='Okke Formsma',
    author_email='okke.formsma@gmail.com',
    url='http://github.com/okke-formsma/vimeo-wrapper',
    packages=['vimeo'],
    install_requires=[
        'requests>=2.0',
        'requests_oauthlib',
        ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        ],
    )