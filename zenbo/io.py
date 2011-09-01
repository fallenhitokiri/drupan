# -*- coding: utf-8 -*-

import os


def read(path, name):
    """
    read file from disc
    <- path: path to file
       name: filename
    -> file content
    """
    f = open(path + os.sep + name)
    c = f.read()
    f.close()

    return c
