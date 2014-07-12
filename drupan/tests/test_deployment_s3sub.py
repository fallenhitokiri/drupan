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
                    "md5path": "asdf",
                    "redirects": "asdf",
                    "site_url": "asdf",
                    "skip_upload": "asdf"
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
        s3d.new_md5s["foo"] = 1
        s3d.compare_md5s()
        self.assertEquals(s3d.changed[0], "foo")

    def test_compare_md5s_changed(self):
        """should add key to changed"""
        s3d = Deploy(self.site, self.config)
        s3d.new_md5s["foo"] = 1
        s3d.old_md5s["foo"] = 2
        s3d.compare_md5s()
        self.assertEquals(s3d.changed[0], "foo")

    def test_compare_md5s_no_change(self):
        """should add key to changed"""
        s3d = Deploy(self.site, self.config)
        s3d.new_md5s["foo"] = 1
        s3d.old_md5s["foo"] = 1
        s3d.compare_md5s()
        self.assertEquals(len(s3d.changed), 0)

    def test_should_upload_skip(self):
        """should skip uploading"""
        s3d = Deploy(self.site, self.config)
        s3d.skip_upload = ["/foo/foo", "bar"]
        s3d.changed = ["/foo/foo"]
        self.assertFalse(s3d.should_upload)

    def test_should_upload(self):
        """should_upload should return True"""
        s3d = Deploy(self.site, self.config)
        s3d.skip_upload = ["foo", "bar"]
        s3d.changed = ["asdf/foo", "bazbaz/zap"]
        self.assertTrue(s3d.should_upload)
