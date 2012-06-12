import os
from setuptools import setup, find_packages

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

setup(
    name='vimeo-wrapper',
    version='0.0.1',
    description='A thin wrapper around requests for vimeo',
    long_description=readme,
    author='Okke Formsma',
    author_email='okke.formsma@gmail.com',
    url='http://github.com/okke-formsma/vimeo-wrapper/tree/master',
    packages=['vimeo'],
    install_requires=[
        'requests',
        'requests-oauth',
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