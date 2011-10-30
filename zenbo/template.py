# -*- coding: utf-8 -*-

"""Template module"""

import sys

from jinja2 import FileSystemLoader, Environment
from jinja2.exceptions import TemplateNotFound

from filters import *


def template(obj, site, env):
    """
    render template
    """
    try:
        template = env.get_template('_' + obj.layout + '.html')
    except TemplateNotFound:
        try:
            template = env.get_template('_' + obj.layout + '.xml')
        except TemplateNotFound:
            print "Template not found: %s" % obj.layout
            sys.exit()
    
    tmp = template.render(obj=obj, site=site)

    return tmp
    

def render(site):
    """
    render objects
    """
    env = Environment(loader = FileSystemLoader(site.template))

    #load filters
    for fil in site.filters:
        env.filters[fil] = getattr(eval(fil), 'handle')

    for key in site.content:
        for cur in site.content[key]:
            cur.rendered = template(cur, site, env)

