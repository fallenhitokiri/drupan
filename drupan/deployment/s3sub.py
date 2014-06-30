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
        self.md5list = config.get_option("s3sub", "md5list")
        self.md5 = dict()
        self.old_md5s = dict()
        self.changed = list()
        self.s3path = "s3://{0}".format(self.bucket)

    def run(self):
        """run the deployment process"""
        self.generate_md5s()
        self.load_md5s()
        self.compare_md5s()
        self.save_md5s()
        self.upload()

    def generate_md5s(self):
        """generate MD5 checksums for all entities"""
        for root, dirs, files in os.walk(self.path):
            for name in files:
                # ignore hidden files
                if name.startswith("."):
                    continue

                filepath = os.path.join(root, name)

                with open(filepath, "rb") as infile:
                    raw = infile.read()
                    self.md5[filepath] = md5(raw).hexdigest()

    def load_md5s(self):
        """load MD5 checksums from disk"""
        with open(self.md5list, "r", encoding="utf-8") as infile:
            raw = infile.read()
            self.old_md5s = json.loads(raw)

    def save_md5s(self):
        """save MD5 checksums to disk"""
        with open(self.md5list, "w", encoding="utf-8") as outfile:
            dumped = json.dumps(self.md5)
            outfile.write(unicode(dumped))

    def compare_md5s(self):
        """compare MD5 checksums"""
        for key in self.md5:
            if not key in self.old_md5s:
                self.changed.append(key)
                continue

            if self.md5[key] != self.old_md5s[key]:
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
