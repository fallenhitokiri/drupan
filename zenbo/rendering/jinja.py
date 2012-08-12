# -*- coding: utf-8 -*-

"""
Render sites using Jinja2

configuration:
  - add name "jinja" to your configuration file
  - add directory that holds the template files

requires:
  - jinja2
"""

from jinja2 import FileSystemLoader, Environment

from jinja_filters import more


class Renderer(object):
    def __init__(self, site):
        self.template_dir = site.path + site.config['rendering']['directory']
        self.site = site

    def render(self):
        env = Environment(loader=FileSystemLoader(self.template_dir))

        env.filters['more'] = getattr(more, 'handle')

        for co in self.site.content:
            template = env.get_template(co.template_name)
            co.rendered = template.render(obj=co, site=self.site)
