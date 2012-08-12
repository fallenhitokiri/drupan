# -*- coding: utf-8 -*-

"""
if there is a more tag return everything above
else return the content string
"""


def handle(content):
    (first, more, second) = content.partition('<!--MORE-->')

    if more == '<!--MORE-->':
        return first
    else:
        return content
