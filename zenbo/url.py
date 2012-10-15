# -*- coding: utf-8 -*-

"""generate nice looking urls"""

import re


def _generate_slug(cobj):
    """clean title for URL generation"""
    if cobj.slug is None:
        # only characters and numbers - everything else becomes a hyphen
        clean = re.sub('[^A-Za-z0-9]+', '-', cobj.meta['title'])

        # multiple '-' do not look nice
        clean = clean.replace('----', '-')
        clean = clean.replace('---', '-')
        clean = clean.replace('--', '-')

        if clean[-1] == "-":
            clean = clean[:-1]

        # last character should never be -
        if clean[-2:-1] == "-":
            clean = clean[:-2]

        # first character should never be a -
        if clean[:1] == "-":
            clean = clean[1:]

        cobj.slug = clean.lower()


def _generate_path(cobj):
    """generate full path. Layout will be provided by cobjnfiguration"""
    # TODO: <sarcasm>add even more complexity</sarcasm>
    layout = cobj.url_scheme

    cobj.meta['year'] = cobj.meta['date'].year
    cobj.meta['month'] = cobj.meta['date'].month
    cobj.meta['day'] = cobj.meta['date'].day

    # split layout. If length of result > 0 check if there are variables
    for key in layout.split("/"):
        if len(key) > 0:
            if key[0] == "$":
                layout = layout.replace(key, str(cobj.meta[key[1:]]))
            if key[0] == "%":
                layout = layout.replace(key, str(getattr(cobj, key[1:])))

    if (len(layout) > 0) and (layout[-1:] is not '/'):
        layout = layout + '/'

    if 'belongs' in cobj.meta:
        cobj.path = cobj.meta['belongs'] + layout
    else:
        cobj.path = layout


def _generate_url(cobj, base):
    """generate full URL"""
    cobj.url = base + cobj.path


def prepare(cobj, site):
    """prepare a content object
    generate slug, path and url
    """
    layouts = site.config.layouts
    (cobj.url_scheme, cobj.template_name) = layouts[cobj.meta['layout']]

    _generate_slug(cobj)
    _generate_path(cobj)
    _generate_url(cobj, site.config.url)
