# -*- coding: utf-8 -*-

from models import content
from generators import *


def generate(site):
    """
    run generators
    <- site object
    """
    for generator in site.generators:
        obj = content.Content()
        gen = getattr(eval(generator), 'generate')(site)
        obj.fromDict(gen, site)
        site.add(obj)
