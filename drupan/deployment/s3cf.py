# -*- coding: utf-8 -*-
"""
    drupan.deployment.s3cf

    Deploying the website to AWS S3 and CloudFront. This plugin will send
    and invalidation request to CloudFront once the deployment is complete,
    invalidating *all* files that changed.

    Using CloudFront invalidation requests can result in high bills. Please
    consider this before using this plugin. If this is a deal breaker use
    s3sub with a 5 minute cache policy.
"""

from hashlib import md5
from mimetypes import MimeTypes

import boto
from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.key import Key

from drupan.file_wrapper import FileWrapper


S3_HOST_ERROR = "buckets name contains a full stop.\n\n"
S3_HOST_ERROR += "Please set the `s3_host` configuration key to your S3 host."


class S3HostMissingException(Exception):
    pass


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
        self.aws_access_key = config.get_option("s3cf", "aws_access_key")
        self.aws_secret_key = config.get_option("s3cf", "aws_secret_key")
        self.cloudfront_id = config.get_option(
            "s3cf",
            "cloudfront_id",
            optional=True,
        )
        self.s3_host = None

        if "." in self.bucket_name:
            try:
                self.s3_host = config.get_option("s3cf", "s3_host")
            except Exception:
                raise S3HostMissingException(S3_HOST_ERROR)

        self.s3_connection = None
        self.bucket = None
        self.cf_connection = None
        self.to_invalidate = list()

        self.redirects = config.get_option("s3cf", "redirects", optional=True)

        if self.redirects is None:
            self.redirects = config.get_option(None, "redirects")

    def run(self):
        """run the deployment process"""
        self.setup()

        self.upload_entities()
        self.upload_assets()
        self.upload_templates()
        self.invalidate()
        self.redirect()

    def setup(self):
        """setup AWS connection"""
        if "." in self.bucket_name:  # work around for a boto bug
            self.s3_connection = S3Connection(
                self.aws_access_key,
                self.aws_secret_key,
                calling_format=OrdinaryCallingFormat(),
                host=self.s3_host,
            )
        else:
            self.s3_connection = S3Connection(
                self.aws_access_key,
                self.aws_secret_key,
            )
        self.bucket = self.s3_connection.get_bucket(self.bucket_name)

        if self.cloudfront_id:
            self.cf_connection = boto.connect_cloudfront(
                self.aws_access_key,
                self.aws_secret_key,
            )

    def upload_entities(self):
        """upload changed files to S3"""
        for entity in self.site.entities:
            self.upload(
                entity.file_path,
                entity.rendered.encode("utf-8"),
                entity.url,
            )
            self.upload_images(entity)

    def upload_images(self, entity):
        """upload all images for this entity

        :param entity: entity to upload images for
        """
        for name in entity.images:
            path = entity.path + "/" + name
            self.upload(path, self.site.images[name])

    def upload_assets(self):
        """upload assets stored in template directory"""
        for name, asset in self.site.assets.items():
            if name.startswith("_"):
                continue

            self.upload(name, asset)

    def upload_templates(self):
        """upload template files which are not prefixed with _"""
        for name, content in self.site.templates.items():
            if name.startswith("_"):
                continue

            self.upload(name, content, name)

    def upload(self, path, content, invalidate=None):
        """
        Set the content, mime type and ACL for a key on S3. Before setting the
        check if the object is new or changed.


        :param path: path for key
        :param content: content to set
        :param invalidate: CloudFront path to add to invalidation list. * will
                           be added to the end to make sure we invalidate the
                           URL path with a trailing slash and the html itself.
                           If None the path will be used.
        """
        changed = self.file_changed(path, content)

        if not changed:
            return

        key = Key(self.bucket)
        key.content_type = guess_mime_type(path)
        key.key = path
        if isinstance(content, FileWrapper):
            key.set_contents_from_string(content.read())
        else:
            key.set_contents_from_string(content)
        key.set_acl("public-read")

        print("uploaded: {0}".format(path))

        if invalidate is None:
            invalidate = path

        self.to_invalidate.append(invalidate + "*")

    def file_changed(self, path, content):
        """
        Check if an keys content is new or changed. If the Key is None the file
        is new, if not compare the etag (MD5) with the checksum of the files
        content.

        Arguments:
            path: key path
            content: content to compare

        Returns:
            True if the key changes or is new and needs to be uploaded and
            invalidated.
        """
        key = self.bucket.get_key(path)

        if not key:
            return True

        if key.etag is None:
            return True

        if isinstance(content, FileWrapper):
            checksum = md5(content.read()).hexdigest()
        else:
            checksum = md5(content).hexdigest()
        return key.etag.replace('"', "") != checksum

    def invalidate(self):
        """Invalidate changed entities"""
        if self.cloudfront_id is None:
            return

        self.cf_connection.create_invalidation_request(
            self.cloudfront_id,
            self.to_invalidate,
        )

        print("invalidating: {0}".format(self.to_invalidate))

    def redirect(self):
        """create a redirect"""
        if self.redirects == dict() or self.redirects is None:
            print("No redirects - skipping.")
            return

        for source, destination in self.redirects.items():
            if self.redirect_exists(source):
                continue

            key = Key(self.bucket)
            key.key = source
            key.set_redirect(destination)
            key.set_acl('public-read')

            print("redirecting: {0} -> {1}".format(source, destination))

    def redirect_exists(self, redirect):
        """
        Check if a redirect exists.

        :param redirect: redirect URL to check

        :returns: True if the redirect already exists
        """
        if self.bucket.get_key(redirect):
            return True
        return False


def guess_mime_type(name):
    """
    Guess the mime type for a filename. Default: binary/octet-stream

    Arguments:
        name: name of the file to return mime type for

    Returns:
        mime type as string
    """
    mime = MimeTypes()
    typ = mime.guess_type(name)[0]

    if typ is None:
        return "binary/octet-stream"

    return typ
