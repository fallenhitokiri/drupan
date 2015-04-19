# -*- coding: utf-8 -*-
"""
    drupan.deployment.s3cf

    Deploying the website to AWS S3 and CloudFront. This plugin will send
    and invalidation request to CloudFront once the deployment is complete,
    invalidating *all* files that changed.

    Using CloudFront invalidation requests can result in high bills. Please
    consider this before using this plugin. If this is a deal breaker use
    s3sub with a 5 minute cache policy.

    Requirement:
        Filesystem writer
"""

from hashlib import md5

import boto
from boto.s3.connection import S3Connection
from boto.s3.key import Key


class Deploy(object):
    def __init__(self, site, config):
        """
        Arguments:
            site: generated site
            config: config for this site
        """
        self.site = site
        self.config = config

        self.bucket_name = config.get_option("s3cf", "bucket")
        self.redirects = config.get_option("s3cf", "redirects")
        self.skip_upload = config.get_option("s3cf", "skip_upload")
        self.aws_access_key = config.get_option("s3cf", "aws_access_key")
        self.aws_secret_key = config.get_option("s3cf", "aws_secret_key")
        self.cloudfront_id = config.get_option("s3cf", "cloudfront_id")

        self.s3_connection = None
        self.bucket = None
        self.cf_connection = None
        self.to_invalidate = list()

    def run(self):
        """run the deployment process"""
        self.setup()

        self.upload()
        self.invalidate()
        self.redirect()

    def setup(self):
        """setup AWS connection"""
        self.s3_connection = S3Connection(
            self.aws_access_key,
            self.aws_secret_key,
        )
        self.bucket = self.s3_connection.get_bucket(self.bucket_name)
        self.cf_connection = boto.connect_cloudfront(
            self.aws_access_key,
            self.aws_secret_key,
        )

    def upload(self):
        """upload changed files to S3"""
        for entity in self.site.entities:
            if not self.entity_changed(entity):
                continue

            key = Key(self.bucket)
            key.key = entity.file_path
            key.set_contents_from_string(entity.rendered)
            key.set_acl('public-read')

            print("uploading: {1}".format(entity.url))

            self.set_invalid(entity)

    def entity_changed(self, entity):
        """
        Check if an entity is new or changed. If the Key is None the file is
        new, else compare the etag (MD5) vs the entities checksum.

        Arguments:
            entity: entity to check

        Returns:
            True if the key changes or is new and needs to be uploaded and
            invalidated.
        """
        key = self.bucket.get_key(entity.file_path)

        if not key:
            return True

        checksum = md5(entity.rendered).hexdigest()
        return key.etag.replace('"', "") == checksum

    def set_invalid(self, entity):
        """
        Add the entities URL and the URL with an inverted slash to the
        invalidation list.

        Arguments:
            entity: entity to invalidate
        """
        self.to_invalidate.append(entity.url)

        if entity.url.endswith("/"):
            self.to_invalidate.append(entity.url[:-1])
        else:
            self.to_invalidate.append("{0}/".format(entity.url))

    def invalidate(self):
        """Invalidate changed entities"""
        self.cf_connection.create_invalidation_request(
            self.cloudfront_id,
            self.to_invalidate,
        )

        print("invalidating: {0}".format(self.to_invalidate))

    def redirect(self):
        """create a redirect"""
        if self.redirects != dict():
            return

        for source in self.redirects:
            if self.redirect_exists(source):
                continue

            destination = self.redirects[source]

            key = Key(self.bucket)
            key.key = source
            key.set_redirect(destination)
            key.set_acl('public-read')

            print("redirecting: {0} -> {1}".format(source, destination))

    def redirect_exists(self, redirect):
        """
        Check if a redirect exists.

        Arguments:
            redirect: redirect URL to check

        Returns:
            True if the redirect already exists
        """
        if not self.bucket.get_key(redirect):
            return True
        return False
