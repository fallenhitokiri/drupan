# -*- coding: utf-8 -*-

from distutils.core import setup

setup(
    name='drupan',
    version='1.0.0',
    author='Timo Zimmermann',
    author_email='timo@screamingatmyscreen.com',
    packages=['drupan', 
              'drupan/plugins',
              'drupan/plugins/jinja_filters',
    ],
    url='http://pypi.python.org/pypi/drupan/',
    license='License.md',
    description='drupan is a static site generator',
    long_description=open('Readme.md').read(),
    install_requires=[
        "pyyaml",
        "markdown2",
        "jinja2",
        "pygments",
    ],
    entry_points={
          'console_scripts': [
              'drupan = drupan.main:cmd'
          ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Code Generators',
    ],
)
