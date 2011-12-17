# -*- coding: utf-8 -*-

#stdlib
import os


listed = os.listdir(os.path.dirname(__file__))
plugins = []

for cur in listed:
    if os.path.splitext(cur)[1] == '.py':
        if cur != '__init__.py':
            plugins.append(os.path.splitext(cur)[0])

__all__ = plugins

