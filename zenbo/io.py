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


def ls(path, ext=None):
    """
    list filesystem
    <- path: path to list
       ext: extensions to filter
    -> array
    """
    files = []

    for cFile in os.listdir(path):
        if ext is not None:
            if os.path.splitext(cFile)[1] == ext:
                files.append(cFile)
        else:
            files.append(cFile)

    return files
                
