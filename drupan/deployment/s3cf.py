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

import os
from hashlib import md5
import json
from io import open

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
        self.path = config.get_option("writer", "directory")
        self.md5_path = config.get_option("s3cf", "md5path")
        self.redirects = config.get_option("s3cf", "redirects")
        self.skip_upload = config.get_option("s3cf", "skip_upload")
        self.aws_access_key = config.get_option("s3cf", "aws_access_key")
        self.aws_secret_key = config.get_option("s3cf", "aws_secret_key")
        self.cloudfront_id = config.get_option("s3cf", "cloudfront_id")

        self.new_md5s = dict()
        self.old_md5s = dict()
        self.changed = list()
        self.s3_connection = None
        self.bucket = None
        self.cf_connection = None

    def run(self):
        """run the deployment process"""
        self.setup()
        self.upload_files()
        self.invalidate()

        # reset - we use the same variables again
        self.new_md5s = dict()
        self.old_md5s = dict()
        self.changed = list()

        self.upload_redirects()

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

    def upload_redirects(self):
        """upload redirects for S3"""
        md5_file = "redirects.md5.json"
        # return if there are no redirects
        if self.redirects == dict():
            return

        self.generate_redirect_md5s()
        self.load_md5(md5_file)
        self.compare_md5s()
        self.save_md5(md5_file)
        self.redirect()

    def upload_files(self):
        """upload generated site to S3"""
        md5_file = "content.md5.json"
        self.generate_site_md5s()
        self.load_md5(md5_file)
        self.compare_md5s()
        self.save_md5(md5_file)

        if self.should_upload:
            self.upload()

    def generate_site_md5s(self):
        """generate MD5 checksums for all entities"""
        for root, dirs, files in os.walk(self.path):
            for name in files:
                # ignore hidden files
                if name.startswith("."):
                    continue

                filepath = os.path.join(root, name)

                with open(filepath, "rb") as infile:
                    raw = infile.read()
                    self.new_md5s[filepath] = md5(raw).hexdigest()

    def generate_redirect_md5s(self):
        """generate MD5 checkusm for all redirects"""
        for redirect in self.redirects:
            self.new_md5s[redirect] = md5(self.redirects[redirect]).hexdigest()

    def load_md5(self, filename):
        """
        load MD5 checksums from disk (json format)

        Arguments:
            filename: name of the file to load MD5 sums from
        """
        load = os.path.join(self.md5_path, filename)

        # if there is no MD5 file, just return
        if not os.path.isfile(load):
            return

        with open(load, "r", encoding="utf-8") as infile:
            raw = infile.read()
            self.old_md5s = json.loads(raw)

    def save_md5(self, filename):
        """
        save MD5 checksums to disk (json format)

        Arguments:
            filename: name of the file to save MD5 sums to
        """
        save = os.path.join(self.md5_path, filename)
        with open(save, "w", encoding="utf-8") as outfile:
            dumped = json.dumps(self.new_md5s)
            outfile.write(unicode(dumped))

    def compare_md5s(self):
        """compare MD5 checksums"""
        for key in self.new_md5s:
            if not key in self.old_md5s:
                self.changed.append(key)
                continue

            if self.new_md5s[key] != self.old_md5s[key]:
                self.changed.append(key)

    def upload(self):
        """upload changed files to S3"""
        for local in self.changed:
            remote = local.replace(self.path, "")
            key = Key(self.bucket)
            key.key = remote
            key.set_contents_from_filename(local)
            key.set_acl('public-read')
            print "uploading: {1}".format(local, remote)

    def invalidate(self):
        invalid = list()

        for local in self.changed:
            url = local.replace(self.path, "")
            invalid.append(url)

        self.cf_connection.create_invalidation_request(
            self.cloudfront_id,
            invalid
        )
        print "invalidating: {0}".format(invalid)

    @property
    def should_upload(self):
        """
        Check if a changed file is part of self.skip_upload. If this
        is the case for all changed files do not upload the site.

        Returns:
            True if the site should be uploaded
        """
        upload = False

        for changed in self.changed:
            url = changed.replace(self.path, "")

            if not url in self.skip_upload:
                upload = True

        return upload

    def redirect(self):
        """create a redirect"""
        for redirect in self.changed:
            # lstrip to make sure joining works if redirect starts with a /
            source = redirect
            destination = self.redirects[redirect]

            key = Key(self.bucket)
            key.key = source
            key.set_redirect(destination)
            key.set_acl('public-read')
            print "redirecting: {0} -> {1}".format(source, destination)
