#!/usr/bin/env python
# coding: utf-8

from setuptools import setup

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name='one_utils',
    version='0.0.1',
    author='onewayforever',
    author_email='onewayforever@163.com',
    url='https://github.com/onewayforever/one-utils',
    description=u'some useful utilities ',
    long_description=long_description,
    long_description_content_type="text/markdown",
    #packages=find_packages(),
    packages=['one_utils'],
    install_requires=[
        'progressbar',
        'pandas',
        'pymysql',
        'sqlalchemy',
        'numpy'
    ]
)
