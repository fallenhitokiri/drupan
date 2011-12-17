# -*- coding: utf-8 -*-

from models import content

from datetime import datetime


def plugin():
    info = {'step' : 'load',
            'description' : 'generate an archive page'}

    return info


def execute(site):
    """
    generate archive
    <- site: site object
    """
    con = site.content['post']

    var = {
            'title'   : 'Archive',
            'layout'  : 'archive',
            'date'    : datetime.now(),
            'content' : con,
        }

    obj = content.Content()
    obj.fromDict(var, site)

    site.add(obj)
