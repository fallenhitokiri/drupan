# -*- coding: utf-8 -*-
"""
    drupan.deployment.gitsub

    Deploy your site via git. Git is called via subprocess.
"""

import datetime
import shlex
import subprocess


CMD_ADD = 'git add .'
CMD_COMMIT = 'git commit -a -m "%s"' % str(datetime.datetime.now())
CMD_PUSH = 'git push -u server master'


class Deploy(object):
    def __init__(self, site, config):
        """
        Arguments:
            site: generated site
            config: config for this site
        """
        self.site = site
        self.config = config

        self.path = config.get_option("gitsub", "path")

    def execute(self, command):
        """
        Execute a command

        Arugments:
            command: command to execute
        """
        proc = subprocess.Popen(shlex.split(command), cwd=self.path)
        proc.communicate()

    def run(self):
        """run the deployment process"""
        self.execute(CMD_ADD)
        self.execute(CMD_COMMIT)
        self.execute(CMD_PUSH)
