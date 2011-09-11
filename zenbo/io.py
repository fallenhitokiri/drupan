# -*- coding: utf-8 -*-

import os
import shutil
import errno


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


def clean(path):
    """
    delete output dir
    <- path
    """
    try:
        shutil.rmtree(path)
    except os.error:
        pass


def copy(template, output):
    """
    copy template dir without _ prefixed files
    <- template: * directory
       output:   * directory
    """
    shutil.copytree(template, output, ignore=shutil.ignore_patterns('_*'))


def mkdir(path):
    """
    create path
    <- path
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            if OSError.errno == errno.EEXIST:
                pass
            else:
                raise


def write(name, content):
    """
    write object to disc
    <- name: file to write
       content: content
    """
    f = open(name, 'w')
    f.write(content)
    f.close()
    
