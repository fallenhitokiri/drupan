This is an alpha release. It should be stable and work as expected but it is
not yet feature complete. Documentation still sucks but you should be able to
figure it out with the quick start section below.

# Zenbo - static site generator
Zenbo is a static site generator. You can use it for blogs, sites or anything
you can imagine. Adding new features is easy thanks to a easy to use plugin
system.

## Quick Start
Copy ```doc/example``` to another location, run ```python path/to/zenbo.py
path/to/example --no-deploy --serve``` and point your browser to ```http://localhost:9000```.

To create additional pages or posts you can find a template for each of them
in ```example/draft/```.

For further details please read ```doc/Details.md```. It should cover everything
you need to know to get a site up and running using Zenbo.

## Features
  - Markdown support
  - Handling images
  - Deploy with git
  - Generate archives and RSS Feeds
  - easily extend it using plugins
  - minimal external dependencies (currently only PyYAML in default distribution)

We use Jinja as template system and you can access everything Zenbo considers
Content in every template. So your imagination is the limit of your site. (Well
beside some technical stuff)

## BETA
Zenbo is considered beta. It "powers" sites that are already used in "production".
Still there could be some bugs. It is tested against Python 2.7, likely not 
compatible to 3.x (see ```finalizers/imagecopy.py```)
