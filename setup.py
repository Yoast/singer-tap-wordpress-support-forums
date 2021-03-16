#!/usr/bin/env python
from setuptools import setup

setup(
    name='tap-wordpress-support-forums',
    version='0.1.0',
    description='Singer.io tap for extracting data',
    author='Stitch',
    url='http://singer.io',
    classifiers=['Programming Language :: Python :: 3 :: Only'],
    py_modules=['tap_wordpress_support_forums'],
    install_requires=[
        'singer-python~=5.12.0',
    ],
    entry_points="""
    [console_scripts]
    tap-wordpress-support-forums=tap_wordpress_support_forums:main
    """,
    packages=['tap_wordpress_support_forums'],
    package_data={
        'schemas': ['tap_wordpress_support_forums/schemas/*.json'],
    },
    include_package_data=True,
)
