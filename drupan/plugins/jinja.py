# -*- coding: utf-8 -*-
"""
    drupan.plugins.jinja

    Plugin to integrate the jinja templating engine.
"""

from jinja2 import FileSystemLoader, Environment


def filter_more(content):
    """
    if there is a more tag return everything above else return the content
    string
    """
    (first, more, second) = content.partition('<!--MORE-->')

    if more == '<!--MORE-->':
        return first
    else:
        return content


class Plugin(object):
    """render site using Jinja"""
    def __init__(self, site, config):
        """
        Arguments:
            site: instance of drupan.site.Site
            config: instance of drupan.config.Config
        """
        self.site = site
        self.config = config

        self.template = config.get_options("jinja", "template")

    def run(self):
        """run the plugin"""
        env = Environment(loader=FileSystemLoader(self.template))

        env.filters['more'] = filter_more

        for page in self.site.entities:
            template = env.get_template(page.layout)
            page.rendered = template.render(
                obj=page,
                site=self.site,
                config=self.config
            )
