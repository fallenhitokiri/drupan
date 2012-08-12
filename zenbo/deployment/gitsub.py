# -*- coding: utf-8 -*-

"""
Deploy homepage with git - subprocess edition
"""

import datetime
import shlex
import subprocess


class Deployment(object):
    def __init__(self, site):
        self.cmd_add = 'git add .'
        self.cmd_commit = 'git commit -m "%s"' % str(datetime.datetime.now())
        self.cmd_push = 'git push -u server master'
        self.path = site.path
        self.site = site

    def _runcommand(self, cmd):
        # TODO: some error handling would be nice
        sp = subprocess.Popen(shlex.split(cmd), cwd=self.path)
        sp.communicate()

    def deploy(self):
        self._runcommand(self.cmd_add)
        self._runcommand(self.cmd_commit)
        self._runcommand(self.cmd_push)
