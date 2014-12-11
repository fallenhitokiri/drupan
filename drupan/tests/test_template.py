# -*- coding: utf-8 -*-
import unittest

from jinja2.exceptions import TemplateNotFound

from drupan.template import Render
from drupan.config import Config
from drupan.entity import Entity
from drupan.site import Site


class TestRender(unittest.TestCase):
    def setUp(self):
        config = Config()
        config.options = {
            "jinja": {
                "template": "foo",
            }
        }

        self.entity = Entity(config)

        site = Site()
        site.entities.append(self.entity)

        self.render = Render(site, config)

    def test_run_skips_empty_layout(self):
        """should not raise an exception - ignore entity"""
        self.render.run()

    def test_template_not_found(self):
        """should raise TemplateNotFound exception"""
        self.entity.meta["layout"] = "foo"
        self.assertRaises(TemplateNotFound, self.render.run)
