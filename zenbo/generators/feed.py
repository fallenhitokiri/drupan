# -*- coding: utf-8 -*-

from datetime import datetime


def generate(site):
    """
    generate feed
    <- site: site object
    -> var: dictionary containing content for object
    """
    con = site.content['post'][:10]

    var = {
            'title'   : 'Feed',
            'layout'  : 'feed',
            'date'    : datetime.now(),
            'content' : con,
        }

    return var
