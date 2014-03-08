# -*- coding: utf-8 -*-

"""
Mock all the things!
"""


class ConfigMock(object):
    def __init__(self):
        self.markdown = {"extras": []}
        self.blank = {
            "entities": [
                {
                    "layout": "index",
                    "menu": False
                },
                {
                    "layout": "archive",
                    "menu": True
                }
            ]
        }


class EntityMock(object):
    def __init__(self):
        self.content = None
        self.raw_content = "foobar"

    @classmethod
    def entries(cls):
        new = [cls()]
        return new


class SiteMock(object):
    def __init__(self):
        self.config = ConfigMock()
        self.entities = EntityMock.entries()
