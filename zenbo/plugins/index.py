# -*- coding: utf-8 -*-

from models import content

from datetime import datetime


def plugin():
    info = {'step' : 'load',
            'description' : 'generate an index object'}

    return info


def execute(site):
    """
    generate index
    <- site: site object
    """
    con = site.content['post'][:5]

    var = {
            'title'   : 'Index',
            'layout'  : 'index',
            'date'    : datetime.now(),
            'content' : con,
        }

    obj = content.Content()
    obj.fromDict(var, site)

    site.add(obj)
