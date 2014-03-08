# -*- coding: utf-8 -*-
import unittest
import sys
import os

import yaml

sys.path.insert(0, os.path.abspath('..'))
from drupan.entity import Entity


class EntityTest(unittest.TestCase):
    def test_from_list(self):
        """should create two new entities"""
        content = ("foo---foo", "bar---bar")
        entities = Entity.from_list(content)

        self.assertEqual(len(entities), 2)

        for entity in entities:
            if not entity.raw in content:
                raise Exception("wrong raw in entity")

    def test_split(self):
        """should split string into meta and content"""
        entity = Entity("foo---bar")
        entity.split()

        self.assertEqual(entity.raw_meta, "foo")
        self.assertEqual(entity.raw_content, "bar")

    def test_parse_yaml(self):
        """should parse header using yaml"""
        test = {"foo": "bar"}

        yamled = yaml.dump(test)

        entity = Entity("")
        entity.raw_meta = yamled
        entity.parse_yaml()

        self.assertEqual(test, entity.meta)
