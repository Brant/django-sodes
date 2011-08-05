import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "django-sodes",
    version = ".1",
    url = 'http://github.com/Brant/django-sodes',
    license = 'GPL',
    description = "Podcast episodes for Django",
    long_description = read('README'),

    author = 'Brant Steen',
    author_email = 'brant.steen@gmail.com',

    packages = find_packages('.'),
    package_dir = {'': '.'},

    install_requires = ['setuptools', 'django'],

    classifiers = [
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPL License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ]
)