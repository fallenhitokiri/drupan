# -*- coding: utf-8 -*-

import shutil
import os
import errno
from io import open


def ensure_separator(directory):
    """path should end on os.sep"""
    if directory[-1:] is not os.sep:
        directory = directory + os.sep
    return directory


def cleandir(directory):
    """remove output directory"""
    try:
        shutil.rmtree(directory)
    except os.error:
        pass


def copytree(indir, outdir, ignore_patterns=None):
    """copy template dir to output dir, ignore '_' files"""
    # TODO: obvious, isn't it?
    if ignore_patterns:
        pattern = ignore_patterns
    else:
        pattern = shutil.ignore_patterns('_*')
    shutil.copytree(indir, outdir, ignore=pattern)


def copyfile(path, name, outdir):
    """copy a file"""
    cfile = ensure_separator(path) + name
    shutil.copy(cfile, outdir)


def mkdir(path):
    """make dir if it does not exist"""
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            if OSError.errno == errno.EEXIST:
                # looks like passing this one is okay
                pass
            else:
                raise


def filelist(directory, extension=None):
    """list all files in a directory"""
    files = []

    for cfile in os.listdir(directory):
        if extension:
            if not os.path.splitext(cfile)[1] == extension:
                continue
        files.append(cfile)

    return files


def read(path, name):
    """read file"""
    full = ensure_separator(path) + name
    read = None
    with open(full, 'r', encoding='utf-8') as infile:
        read = infile.read()
    return read


def write(name, content):
    """write file"""
    with open(name, 'w', encoding='utf-8') as output:
        output.write(content)
