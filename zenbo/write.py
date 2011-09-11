# -*- coding: utf-8 -*-

import io


def write(site):
    """
    write content to disc
    <- site object
    """
    io.clean(site.output)
    io.copy(site.template, site.output)

    for key in site.content:
        for obj in site.content[key]:
            obj.url = obj.url.replace(site.url, '')
            
            if len(obj.url.split('/')) > 1:
                path = "%s/%s" % (site.output, obj.url.rsplit('/', 1)[0])
                io.mkdir(path)

            name    = "%s/%s" % (site.output, obj.url)

            io.write(name, obj.rendered)
    
