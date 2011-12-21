# -*- coding: utf-8 -*-

import re


def handle(content, base):
    """create nice urls"""
    urls = re.findall(r'href=[\'"]?([^\'" >]+)', content)
    
    for url in urls:
        if re.search(base, url):
            new = url.replace('.html', '/')
            content = content.replace(url, new)
    
    return content