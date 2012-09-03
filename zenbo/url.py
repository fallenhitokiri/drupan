# -*- coding: utf-8 -*-

"""
generate nice looking urls
"""

def _generate_slug(co):
    # this should be regex magic
    if co.slug is None:
        t = co.meta['title']
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

        co.slug = t.lower()

def _generate_path(co):
    # TODO: <sarcasm>add even more complexity</sarcasm>
    layout = co.url_scheme

    co.meta['year'] = co.meta['date'].year
    co.meta['month'] = co.meta['date'].month
    co.meta['day'] = co.meta['date'].day

    # split layout. If length of result > 0 check if there are variables
    for key in layout.split("/"):
        if len(key) > 0:
            if key[0] == "$":
                layout = layout.replace(key, str(co.meta[key[1:]]))
            if key[0] == "%":
                layout = layout.replace(key, str(getattr(co, key[1:])))

    if (len(layout) > 0) and (layout[-1:] is not '/'):
        layout = layout + '/'

    if 'belongs' in co.meta:
        co.path = co.meta['belongs'] + layout
    else:
        co.path = layout

def _generate_url(co, base):
    co.url = base + co.path

def prepare(co, site):
    layouts = site.config['layouts']
    (co.url_scheme, co.template_name) = layouts[co.meta['layout']]

    _generate_slug(co)
    _generate_path(co)
    _generate_url(co, site.config['url'])
