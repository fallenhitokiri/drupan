# -*- coding: utf-8 -*-

from models import content

from datetime import datetime


def plugin():
    info = {'step' : 'load',
            'description' : 'generate a rss feed'}

    return info


def execute(site):
    """
    generate feed
    <- site: site object
    """
    con = site.content['post'][:10]
    now = datetime.now()

    var = {
            'title'   : 'Feed',
            'layout'  : 'feed',
            'date'    : now,
            'rfc'     : now.strftime('%a, %d %b %Y %H:%M:%S'),
            'content' : con,
        }

    obj = content.Content()
    obj.fromDict(var, site)

    site.add(obj)
