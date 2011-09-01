# -*- coding: utf-8 -*-

from datetime import datetime


def generate(site):
    """
    generate archive
    <- site: site object
    -> var: dictionary containing content for object
    """
    con = site.content['post']

    var = {
            'title'   : 'Archive',
            'layout'  : 'archive',
            'date'    : datetime.now(),
            'content' : con,
        }

    return var
