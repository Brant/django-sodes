from setuptools import setup, find_packages



setup(
    name = "django-sodes",
    version = ".1",
    url = 'http://github.com/Brant/django-sodes',
    license = 'GPL',
    description = "Podcast episodes for Django",
    long_description = open('README').read(),

    author = 'Brant Steen',
    author_email = 'brant.steen@gmail.com',
    
    install_requires = ['setuptools', 'django', ],
    
    
    packages = find_packages(exclude=('tests', )),
    include_package_data = True,
    zip_safe = False,
    

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