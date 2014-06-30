# -*- coding: utf-8 -*-
import unittest

from drupan.site import Site
from drupan.config import Config
from drupan.deployment.s3sub import Deploy


class TestS3Sub(unittest.TestCase):
    def setUp(self):
        self.site = Site()
        self.config = Config()
        cfg = {
            "options": {
                "s3sub": {
                    "bucket": "asdf",
                    "profile": "asdf",
                    "md5list": "asdf"
                },
                "writer": {
                    "directory": "asdf"
                }
            }
        }
        self.config.from_dict(cfg)

    def test_compare_md5s_not_found(self):
        """should add key to changed"""
        s3d = Deploy(self.site, self.config)
        s3d.md5["foo"] = 1
        s3d.compare_md5s()
        self.assertEquals(s3d.changed[0], "foo")

    def test_compare_md5s_changed(self):
        """should add key to changed"""
        s3d = Deploy(self.site, self.config)
        s3d.md5["foo"] = 1
        s3d.old_md5s["foo"] = 2
        s3d.compare_md5s()
        self.assertEquals(s3d.changed[0], "foo")

    def test_compare_md5s_no_change(self):
        """should add key to changed"""
        s3d = Deploy(self.site, self.config)
        s3d.md5["foo"] = 1
        s3d.old_md5s["foo"] = 1
        s3d.compare_md5s()
        self.assertEquals(len(s3d.changed), 0)
