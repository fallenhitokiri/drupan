# -*- coding: utf-8 -*-
"""
    drupan.deployment.s3sub

    Deploy your site to AWS S3. The AWS cli tool is called via subprocess.
"""

import subprocess


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

    def run(self):
        """run the deployment process"""
        s3path = "s3://{0}".format(self.bucket)
        proc = subprocess.Popen(
            [
                "aws",
                "s3",
                "sync",
                ".",
                s3path,
                "--delete",
                "--profile",
                self.profile
            ],
            cwd=self.path
        )
        proc.communicate()
