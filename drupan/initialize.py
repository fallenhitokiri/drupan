# -*- coding: utf-8 -*-

"""
    drupan.initialize

    Initializes a new site.
"""

import os
import shutil
import sys


INSTRUCTIONS = """Your new site was created.

To build your new site change to the directory and run

drupan config.yaml --serve

For more information on how to correctly configure your site and what
plugins you can use please read the quickstart guide at
http://github.com/fallenhitokiri/drupan/docs/quickstart.md

Enjoy drupan :)
"""


def bootstrap(path):
    """
    Copy the template for new sites to the given path. Only copy if the path
    does not exist.

    Arguments:
        path: path to copy the new site to
    """
    base = os.path.dirname(os.path.realpath(__file__))
    template = os.path.join(base, "bootstrap-template")

    if os.path.exists(path):
        print "path already exists. Please specify one that does not exist."
        sys.exit()

    shutil.copytree(template, path)

    print INSTRUCTIONS
