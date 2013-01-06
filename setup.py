from distutils.core import setup

description="""
Long polling requests for for Django 1.3+ using gevent
"""

setup(
    name="django_longpolling",
    version='0.0.1',
    url='https://github.com/tbarbugli/django_longpolling',
    license='BSD',
    platforms=['OS Independent'],
    description = description.strip(),
    author = 'Tommaso Barbugli',
    author_email = 'tbarbugli@gmail.com',
    maintainer = 'Tommaso Barbugli',
    maintainer_email = 'tbarbugli@gmail.com',
    packages = [
        'django_longpolling',
    ],
    requires = [
        'gevent',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
    ]
)