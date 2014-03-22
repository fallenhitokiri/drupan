# -*- coding: utf-8 -*-
import unittest

from drupan.config import Config
from drupan.site import Site
from drupan.entity import Entity
from drupan.plugins.markdown import Plugin


RAW = """
foobar

```python
if True
```
"""

RAW_MARKUP = """
<p>foobar</p>\n\n<div class="codehilite"><pre><code><span class="k">
if</span> <span class="bp">True</span>\n</code></pre></div>\n"""


class TestMarkdown(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.config.options = {
            "markdown": {
                "extras": "."
            }
        }

        self.site = Site()

        self.entity = Entity(self.config)
        self.entity.raw = "foobar"

    def test_convert(self):
        """should convert a string to markdown"""
        plugin = Plugin(self.site, self.config)
        plugin.convert(self.entity)

        self.assertNotEqual(self.entity.content, None)
        self.assertEqual(self.entity.content, "<p>foobar</p>\n")

    def test_convert_syntax(self):
        """should add a code block"""
        self.config.options["markdown"]["extras"] = ["fenced-code-blocks"]
        self.entity.raw = RAW
        plugin = Plugin(self.site, self.config)
        plugin.convert(self.entity)

        expected = RAW_MARKUP.translate(None, "\n")
        result = str(self.entity.content).translate(None, "\n")

        self.assertNotEqual(self.entity.content, None)
        self.assertEqual(expected, result)
