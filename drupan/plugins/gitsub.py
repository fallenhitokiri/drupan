# -*- coding: utf-8 -*-

import datetime
import shlex
import subprocess


class Feature(object):
    """Deploy homepage with git - subprocess edition"""
    def __init__(self, site):
        self.cmd_add = 'git add .'
        self.cmd_commit = 'git commit -m "%s"' % str(datetime.datetime.now())
        self.cmd_push = 'git push -u server master'
        self.path = site.path
        self.no_deployment = site.no_deployment
        self.site = site

    def _runcommand(self, cmd):
        """run a command"""
        # TODO: some error handling would be nice
        sp = subprocess.Popen(shlex.split(cmd), cwd=self.path)
        sp.communicate()

    def run(self):
        """deploy site
        - add
        - commit
        - push
        """
        if not self.no_deployment:
            self._runcommand(self.cmd_add)
            self._runcommand(self.cmd_commit)
            self._runcommand(self.cmd_push)
