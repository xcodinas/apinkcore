import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="APInkcore",
    version="0.0.1",
    author="Xavier Codinas",
    author_email="xavier19966@gmail.com",
    description=("Api for HACKEPS."),
    license="BSD",
    packages=['app'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'Flask-sqlalchemy',
        'Flask-migrate',
        'Flask-script',
        'Flask-restful',
        'Flask-jwt-extended',
        'passlib',
        'sentry-sdk[flask]==0.8.0',
    ],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    test_suite='tests',
)
