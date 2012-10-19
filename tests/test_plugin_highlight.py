#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
from drupan.plugins import highlight


TEST_DATA = """<pre><code>#!/usr/bin/env python

print "hallo welt"
"""

EXPECTED_OUTPUT = """<pre><code><table class="highlighttable"><tr><td class="linenos"><div class="linenodiv"><pre>1
2
3</pre></div></td><td class="code"><div class="highlight"><pre><span class="c">#!/usr/bin/env python</span>

<span class="k">print</span> <span class="s">&quot;hallo welt&quot;</span>
</pre></div>
</td></tr></table>"""


class Obj(object):
    """small content object"""
    def __init__(self):
        self.content = "foo"
        self.markup = TEST_DATA


class Config(object):
    def options_for_key(self, key):
        return {}


class So(object):
    """small site object"""
    def __init__(self):
        co = Obj()
        cfg = Config()
        self.content = [co]
        self.config = cfg


class ValidHighlightTest(unittest.TestCase):
    def test_highlight(self):
        site = So()
        content = site.content[0].markup
        plugin = highlight.Feature(site)
        plugin.run()
        self.assertEqual(site.content[0].markup, EXPECTED_OUTPUT)


def main():
    unittest.main()


if __name__ == '__main__':
    main()
