# coding: utf-8

from io import ls
from models import content


def load(site):
    """
    load content from disc
    <- site object
    """
    for cFile in ls(site.input, site.extension):
        obj = content.Content()
        obj.fromFile(cFile, site)
        site.add(obj)
