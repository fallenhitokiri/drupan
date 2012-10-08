# -*- coding: utf-8 -*-

from datetime import datetime


class ContentObject(object):
    """One ContentObject represents one page of the site"""
    def __init__(self):
        self.meta = {}  # informations about this object from source
        self.content = None  # input content
        self.slug = None  # slug for URL
        self.url = None  # full url
        self.path = None  # full path to file of content object
        self.menu = False  # should appear in menu?
        self.markup = None  # content after running markup plugin
        self.url_scheme = None  # url scheme (from config)
        self.template_name = None  # template name to render this ContentObject
        self.rendered = None  # finished object

    def add_meta(self, title, layout, menu=False):
        """add meta data if a content object is generated"""
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
