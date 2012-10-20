drupan - formerly known as Zenbo.

# drupan - static site generator
drupan is a static site generator. You can use it for blogs, sites or anything
you can imagine. Adding new features is easy thanks to a easy to use plugin
system.

## Quick Start
If you want to make sure you have all dependencies installed run 
```pip install -r requirements.txt```.

Run ```drupan.py --init path-to-site```. You find a template for a post or a
page in your new sites path in the directory ```draft```.

Run ```drupan.py path-to-site --no-deploy --serve``` and visit your new site
on ```http://localhost:9000```.

## Features
  - Markdown support
  - Image support
  - Deploy with git
  - Generate archives and RSS Feeds
  - Easily extend it using plugins
  - Minimal external dependencies

### Jinja
We use Jinja as template system and you can access everything drupan considers
Content in every template. So your imagination is the limit of your site. (Well
beside some technical stuff)

### Dependencies
  - PyYAML
  - Jinja2
  - markdown2
  - pygments

If you do not want to use Jinja as templating engine or markdown for your posts
you can deactive both plugins in your configuration file and ignore the packages.
They are only needed by the corresponding plugin.

## BETA
drupan is considered beta. It "powers" sites that are already used in "production".
Still there could be some bugs. It is tested against Python 2.7, likely not 
compatible to 3.x (see ```plugins/imagecopy.py```)
