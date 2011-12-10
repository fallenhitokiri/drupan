# -*- coding: utf-8 -*-

from datetime import datetime


def generate(site):
    """
    generate feed
    <- site: site object
    -> var: dictionary containing content for object
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

    return var
