# -*- coding: utf-8 -*-

from jinja2 import FileSystemLoader, Environment

from drupan.plugins.jinja_filters import more


class Feature(object):
    """render site using Jinja"""
    def __init__(self, site):
        self.site = site
        self.template_dir = site.config.template

    def run(self):
        """run the plugin"""
        env = Environment(loader=FileSystemLoader(self.template_dir))

        env.filters['more'] = getattr(more, 'handle')

        for cobj in self.site.content:
            template = env.get_template(cobj.template_name)
            cobj.rendered = template.render(obj=cobj, site=self.site)
