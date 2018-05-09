# -*- coding: utf-8 -*-
"""
    drupan.template

    Integrate the jinja template engine.
"""

from jinja2 import DictLoader, Environment


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


def filter_filter(site, key, value):
    """
    returns one or more entities for a specific key / value combination. Uses
    Site.get()
    """
    filtered = site.get(key, value)

    if type(filtered) != list:
        return [filtered]

    return filtered


def filter_get(site, key, value):
    """
    returns one entity for a specific key / value combination. Uses Site.get()
    """
    filtered = site.get(key, value)

    if type(filtered) == list:
        raise Exception("too many results", key, value)
    if filtered is None:
        raise Exception("no result for", key, value)

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

    def run(self):
        """run the plugin"""
        env = Environment(
            loader=DictLoader(self.site.templates),
            extensions=["jinja2.ext.with_", "jinja2.ext.do"]
        )

        env.filters["more"] = filter_more
        env.filters["filter"] = filter_filter
        env.filters["get"] = filter_get

        for page in self.site.entities:
            if not page.layout:
                continue

            name = "_{0}.html".format(page.layout)
            template = env.get_template(name)
            page.rendered = template.render(
                obj=page,
                site=self.site,
                config=self.config
            )
