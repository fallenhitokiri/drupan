# -*- coding: utf-8 -*-

import markdown2 as md


def markup(content):
    """
    run content thru markdown
    <- content: content form object
    -> content: content after markdown magic
    """
    content = md.markdown(content)

    return content

