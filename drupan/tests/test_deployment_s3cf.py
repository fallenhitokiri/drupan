# -*- coding: utf-8 -*-
import unittest

from mock import patch

from drupan.site import Site
from drupan.config import Config
from drupan.deployment.s3cf import (
    Deploy,
    S3HostMissingException,
    guess_mime_type,
)


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

    def test_init_missing_bucket(self):
        """
        should raise an exception if there is a dot in the bucket name and not
        s3_host specified
        """
        self.config.options["s3cf"]["bucket"] = "foo.bar"

        self.assertRaises(
            S3HostMissingException,
            Deploy,
            self.site,
            self.config,
        )

        self.config.options["s3cf"]["s3_host"] = "foo"

        Deploy(self.site, self.config)

    def test_guess_mime_type(self):
        """should guess the correct mime type"""
        self.assertEqual(guess_mime_type("foo"), "binary/octet-stream")
        self.assertEqual(guess_mime_type("foo.jpg"), "image/jpeg")
        self.assertEqual(guess_mime_type("foo.png"), "image/png")
        self.assertEqual(guess_mime_type("foo.html"), "text/html")
        self.assertEqual(guess_mime_type("foo.css"), "text/css")

    def test_redirects(self):
        """should always get the correct redirects"""
        deploy = Deploy(self.site, self.config)
        self.assertEqual(deploy.redirects, "asdf")

        self.config.redirects = "1234"
        self.config.options["s3cf"]["redirects"] = None
        deploy = Deploy(self.site, self.config)
        self.assertEqual(deploy.redirects, "1234")

    def test_redirect_exists(self):
        """should return True if a redirect exists, False if not"""
        class BucketMock(object):
            @classmethod
            def get_key(cls, redirect):
                return redirect

        deploy = Deploy(self.site, self.config)
        deploy.bucket = BucketMock()
        self.assertTrue(deploy.redirect_exists(True))
        self.assertFalse(deploy.redirect_exists(False))

    @patch("drupan.deployment.s3cf.Deploy.upload")
    def test_upload_assets(self, mock):
        """should only add one asset to the upload dictionary"""
        deploy = Deploy(self.site, self.config)
        deploy.site.assets["foo"] = "foo"
        deploy.site.assets["_bar"] = "bar"
        deploy.upload_assets()

        mock.assert_called_once_with("foo", "foo")
