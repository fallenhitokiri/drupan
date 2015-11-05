"""
drupan - flexible static site generator
---------------------------------------

Drupan is a flexible static site generator helping you to create blogs, single
page applications or traditional websites. While being opinionated the plugin
system allows you to extend it with any functionality you desire.

Quickstart
``````````

Install drupan, clone the example site (see links section)
repository and run `drupan config.yaml --serve` in the cloned directory.

Noteworthy Features
```````````````````

* deployment your site using git or directly to AWS S3 and AWS CloudFront
* fast page generation
* Jinja2 with custom template tags and filters
* powerful plugin system

Usage
`````

You can install drupan via pip. To generate your site you just run
`drupan ~path/to/config.yaml`.

Supported command line switches

* `nodeploy` do not deploy the generated site
* `serve` runs a development server on port 9000
* `deploy` deploy your output directory without generation

Readers
```````

* `filesystem` reads content from files with a YAML header

Writers
```````

* `filesystem` writes the generated site to a directory

Deployment
``````````

* `s3cf` deploy your site to AWS S3 and optionally invalidate changed files on AWS CloudFront using both
* `gitsub` commits the changes to git and pushes to a remote server
* `s3sub` uploads your site to AWS S3 using the AWS CLI package

Plugins
```````

* `blank` generates empty Entity instances with a given layout. This can be used to generate index or archive pages
* `markdown` converts entity content from markdown to HTML
* `tags` support for tags which are added to a posts meta information

Links
`````

* `development version <https://github.com/fallenhitokiri/drupan/>`_
* `example site <https://github.com/fallenhitokiri/drupan-template-blog/>`_

"""
from distutils.core import setup

from drupan.version import __version__



setup(
    name="drupan",
    version=__version__,
    author="Timo Zimmermann",
    author_email="timo@screamingatmyscreen.com",
    packages=[
        "drupan",
        "drupan/plugins",
        "drupan/deployment",
        "drupan/inout"
    ],
    url="http://pypi.python.org/pypi/drupan/",
    license="BSD",
    description="Drupan is a flexible static site generator helping you \
    to create blogs, single page applications or traditional websites.",
    long_description=__doc__,
    install_requires=[
        "pyyaml",
        "markdown2",
        "jinja2",
        "pygments",
    ],
    entry_points={
        "console_scripts": [
            "drupan = drupan.cmd:cmd"
        ]
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
    ],
)
