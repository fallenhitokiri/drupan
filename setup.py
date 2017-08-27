from distutils.core import setup

from drupan.version import __version__

try:
    import pypandoc
    long_description = pypandoc.convert("Readme.md", "rst")
except:
    long_description = "Readme not found"


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
    long_description=long_description,
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
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Software Development :: Code Generators",
    ],
)
