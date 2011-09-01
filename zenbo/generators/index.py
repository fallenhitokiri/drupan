# -*- coding: utf-8 -*-

from datetime import datetime


def generate(site):
    """
    generate index
    <- site: site object
    -> var: dictionary containing content for object
    """
    con = site.content['post'][:5]

    var = {
            'title'   : 'Index',
            'layout'  : 'index',
            'date'    : datetime.now(),
            'content' : con,
        }

    return var
