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

    def _generate_slug(self):
        #this should be regex magic
        if self.slug is None:
            t = self.meta['title']
            t = t.replace(' ', '-')
            t = t.replace('.', '-')
            t = t.replace('!', '-')
            t = t.replace('?', '-')
            t = t.replace('&', '-')
            t = t.replace(';', '-')
            t = t.replace(':', '-')
            t = t.replace('#', '-')
            t = t.replace('~', '-')
            t = t.replace('*', '-')
            t = t.replace('`', '-')
            t = t.replace('\'', '-')
            t = t.replace("\"", "-")
            t = t.replace('$', '-')
            t = t.replace('@', '-')
            t = t.replace('%', '-')
            t = t.replace('/', '-')
            t = t.replace('(', '-')
            t = t.replace(')', '-')
            t = t.replace('[', '-')
            t = t.replace(']', '-')
            t = t.replace('{', '-')
            t = t.replace('}', '-')
            t = t.replace('=', '-')
            t = t.replace('^', '-')
            t = t.replace('<', '-')
            t = t.replace('>', '-')
            t = t.replace('|', '-')

            t = t.replace('----', '-')
            t = t.replace('---', '-')
            t = t.replace('--', '-')

            if t[-1] == "-":
                t = t[:-1]

            # last character should never be -
            if t[-2:-1] == "-":
                t = t[:-2]

            self.slug = t.lower()

    def _generate_path(self):
        # TODO: <sarcasm>add even more complexity</sarcasm>
        layout = self.url_scheme

        self.meta['year'] = self.meta['date'].year
        self.meta['month'] = self.meta['date'].month
        self.meta['day'] = self.meta['date'].day

        # split layout. If length of result > 0 check if there are variables
        for key in layout.split("/"):
            if len(key) > 0:
                if key[0] == "$":
                    layout = layout.replace(key, str(self.meta[key[1:]]))
                if key[0] == "%":
                    layout = layout.replace(key, str(getattr(self, key[1:])))

        if (len(layout) > 0) and (layout[-1:] is not '/'):
            layout = layout + '/'

        self.path = layout

    def _generate_url(self, base):
        self.url = base + self.path

    def prepare(self, site):
        layouts = site.config['layouts']
        (self.url_scheme, self.template_name) = layouts[self.meta['layout']]

        self._generate_slug()
        self._generate_path()
        self._generate_url(site.config['url'])

    def __unicode__(self):
        if self.slug is not None:
            return self.slug
        else:
            return self.meta['title']

    def __str__(self):
        return unicode(self).encode('utf-8')
