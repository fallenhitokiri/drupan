# -*- coding: utf-8 -*-
import unittest

from drupan.site import Site
from drupan.config import Config
from drupan.deployment.s3cf import Deploy
from drupan.entity import Entity


class TestS3cf(unittest.TestCase):
    def setUp(self):
        self.site = Site()
        self.config = Config()
        cfg = {
            "options": {
                "s3cf": {
                    "bucket": "asdf",
                    "md5path": "asdf",
                    "redirects": "asdf",
                    "site_url": "asdf",
                    "skip_upload": "asdf",
                    "aws_access_key": "asdf",
                    "aws_secret_key": "asdf",
                    "cloudfront_id": "asdf",
                },
            }
        }
        self.config.from_dict(cfg)

    def test_set_invalid(self):
        """should set two urls"""
        s3cf = Deploy(self.site, self.config)
        entity = Entity(self.config)
        entity._url = "/foo/bar/"
        s3cf.set_invalid(entity)
        self.assertEqual(len(s3cf.to_invalidate), 2)
        self.assertEqual(s3cf.to_invalidate[1], "/foo/bar")
