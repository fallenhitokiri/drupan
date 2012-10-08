# -*- coding: utf-8 -*-


def handle(content):
    """if there is a more tag return everything above
    else return the content string
    """
    (first, more, second) = content.partition('<!--MORE-->')

    if more == '<!--MORE-->':
        return first
    else:
        return content
