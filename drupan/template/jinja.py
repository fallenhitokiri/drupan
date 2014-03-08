# -*- coding: utf-8 -*-

"""
drupan.template.jinja

Templating engine using jinja.
"""

from jinja2 import FileSystemLoader, Environment


def more_filter(content):
    """if there is a "more" tag return everything above it"""
    (first, more, second) = content.partition('<!--MORE-->')

    if more == '<!--MORE-->':
        return first
    else:
        return content


class TemplateEngine(object):
    """render site using Jinja"""
    def __init__(self, site):
        self.site = site
        self.configure()

    def configure(self):
        """check that this is template engine configured properly"""
        if not hasattr(self.site.config, "jinja"):
            raise Exception("Jinja isn't configured properly")

        self.config = self.site.config.jinja

        if not "template" in self.config:
            raise Exception("Jinja isn't configured properly")

        self.template = self.config["template"]

    def run(self):
        """run the engine"""
        env = Environment(loader=FileSystemLoader(self.template))

        env.filters['more'] = getattr(more_filter, 'handle')

        for entity in self.site.entities:
            template = env.get_template(entity.template_name)
            entity.rendered = template.render(obj=entity, site=self.site)
