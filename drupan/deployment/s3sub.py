# -*- coding: utf-8 -*-
"""
    drupan.deployment.s3sub

    Deploy your site to AWS S3. The AWS cli tool is called via subprocess.

    Requirement:
        Filesystem writer
"""

import subprocess
from hashlib import md5
import json
from io import open
import os
from urlparse import urljoin


class Deploy(object):
    def __init__(self, site, config):
        """
        Arguments:
            site: generated site
            config: config for this site
        """
        self.site = site
        self.config = config

        self.bucket = config.get_option("s3sub", "bucket")
        self.profile = config.get_option("s3sub", "profile")
        self.path = config.get_option("writer", "directory")
        self.md5_path = config.get_option("s3sub", "md5path")
        self.redirects = config.get_option("s3sub", "redirects")
        self.site_url = config.get_option("s3sub", "site_url")
        self.skip_upload = config.get_option("s3sub", "skip_upload")

        self.new_md5s = dict()
        self.old_md5s = dict()
        self.changed = list()
        self.s3path = "s3://{0}".format(self.bucket)

    def run(self):
        """run the deployment process"""
        self.upload_files()

        # reset - we use the same variables again
        self.new_md5s = dict()
        self.old_md5s = dict()
        self.changed = list()

        self.upload_redirects()

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
            remote = local.replace(self.path, self.s3path)

            proc = subprocess.Popen(
                [
                    "aws",
                    "s3",
                    "cp",
                    local,
                    remote,
                    "--profile",
                    self.profile
                ],
                cwd=self.path
            )
            proc.communicate()

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
        index = os.path.join(self.path, "index.html")

        for redirect in self.changed:
            # lstrip to make sure joining works if redirect starts with a /
            source = os.path.join(self.s3path, redirect.lstrip("/"))
            destination = urljoin(self.site_url, self.redirects[redirect])

            proc = subprocess.Popen(
                [
                    "aws",
                    "s3",
                    "cp",
                    index,
                    source,
                    "--website-redirect",
                    destination,
                    "--profile",
                    self.profile
                ],
                cwd=self.path
            )
            proc.communicate()
