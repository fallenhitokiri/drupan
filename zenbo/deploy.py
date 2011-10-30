# -*- coding: utf-8 -*-

from deployment import *


def deploy(site):
    """
    deploy generated site
    <- site object
    """
    getattr(eval(site.deployment['type']), 'publish')(site)
