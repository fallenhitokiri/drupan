# -*- coding: utf-8 -*-

import shlex, subprocess
from datetime import datetime


def __exec(cmd, path):
    """execute git command"""
    sp = subprocess.Popen(shlex.split(cmd), cwd=path)
    sp.communicate()
        

def _add(path):
    """add new files to git"""
    cmd = 'git add .'
    __exec(cmd, path)
        

def _commit(path):
    """commit files"""
    cmd = 'git commit -m "%s"' % str(datetime.now())
    __exec(cmd, path)
        

def _push(path):
    """push repo to server"""
    cmd = 'git push -u server master'
    __exec(cmd, path)
        
    
def publish(site):
    """
    publish site
    <- site object
    """
    path = str(site.path)
    _add(path)
    _commit(path)
    _push(path)
    
