# -*- coding: utf-8 -*-

from datetime import datetime


class ContentObject(object):
    def __init__(self):
        self.meta = {}
        self.content = None
        self.slug = None
        self.url = None
        self.path = None
        self.menu = False
        self.markup = None
        self.url_scheme = None
        self.template_name = None
        self.rendered = None

    def add_meta(self, title, layout, menu=False):
        self.meta['title'] = title
        self.meta['date'] = datetime.now()
        self.meta['layout'] = layout
        self.menu = menu

    def __unicode__(self):
        if self.slug is not None:
            return self.slug
        else:
            return self.meta['title']

    def __str__(self):
        return unicode(self).encode('utf-8')
