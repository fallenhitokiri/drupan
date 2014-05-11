# -*- coding: utf-8 -*-
"""
    drupan.template

    Integrate the jinja templating engine.
"""

from jinja2 import FileSystemLoader, Environment


def filter_more(content):
    """
    if there is a more tag return everything above else return the content
    string
    """
    (first, more, second) = content.partition("<!--MORE-->")

    if more == "<!--MORE-->":
        return first
    else:
        return content


def filter_filter(entities, key, value):
    """filter entities based on key and value"""
    filtered = []

    for entity in entities:
        if getattr(entity, key) == value:
            filtered.append(entity)

    return filtered


class Render(object):
    """render site using Jinja"""
    def __init__(self, site, config):
        """
        Arguments:
            site: instance of drupan.site.Site
            config: instance of drupan.config.Config
        """
        self.site = site
        self.config = config

        self.template = config.get_option("jinja", "template")

    def run(self):
        """run the plugin"""
        env = Environment(loader=FileSystemLoader(self.template))

        env.filters["more"] = filter_more
        env.filters["filter"] = filter_filter

        for page in self.site.entities:
            name = "_{0}.html".format(page.layout)
            template = env.get_template(name)
            page.rendered = template.render(
                obj=page,
                site=self.site,
                config=self.config
            )
