# -*- coding: utf-8 -*-

# see: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='armor',
    version='0.1.0',
    description='Pandoc wrapped in styles',
    long_description=readme,
    author='Sebastian Bogan',
    author_email='sebogh@qibli.net',
    url='https://github.com/sebogh/armor',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)

