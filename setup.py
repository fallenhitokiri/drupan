# -*- coding: utf-8 -*-

from distutils.core import setup

from drupan.version import __version__


LONGDESC = """======
drupan
======

drupan is a static site generator. You can use it for blogs, sites or anything
you can imagine. Adding new features is easy thanks to a easy to use plugin
system.

Quick Start
===========
Run ```drupan --init path-to-site```. You find a template for a post or a
page in your new sites path in the directory ```draft```.

Run ```drupan path-to-site --no-deploy --serve``` and visit your new site
on ```http://localhost:9000```.

Features
========
  - Markdown support
  - Image support
  - Deploy with git
  - Generate archives and RSS Feeds
  - Easily extend it using plugins
  - Minimal external dependencies
  - syntax highlighting using pygments

Jinja
-----
drupan uses Jinja as template system and you can access everything drupan considers
Content in every template. So your imagination is the limit of your site. (Well
beside some technical stuff)

Dependencies
============
  - PyYAML
  - Jinja2
  - markdown2
  - pygments

If you do not want to use Jinja as templating engine or markdown for your posts
you can deactive both plugins in your configuration file and ignore the packages.
They are only needed by the corresponding plugin.
"""


setup(
    name='drupan',
    version=__version__,
    author='Timo Zimmermann',
    author_email='timo@screamingatmyscreen.com',
    packages=['drupan',
              'drupan/plugins',
              'drupan/plugins/jinja_filters',
    ],
    url='http://pypi.python.org/pypi/drupan/',
    license='BSD',
    description='drupan is a static site generator',
    long_description=LONGDESC,
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
