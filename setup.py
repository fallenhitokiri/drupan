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
)