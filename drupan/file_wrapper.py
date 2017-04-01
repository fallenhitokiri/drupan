# -*- coding: utf-8 -*-


class FileWrapper(object):
    """FileWrapper provides an interface to move files through drupan.

    Every reader plugin should wrap files, like images, in an instance  of a
    class which inherits FileWrapper which provides memory efficient access to
    the files content.

    Every plugin that needs to know if it is dealing with a file should check
    if the variable is an instance of FileWrapper.
    """
    def read(self):
        """:returns: content of the file"""
        raise NotImplementedError()
