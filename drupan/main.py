# -*- coding: utf-8 -*-
import argparse

from drupan import core
from drupan.version import __version__


def cmd():
    """command line entry point"""
    desc = "drupan v{0}".format(__version__)
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('path', help='path to configuration file')
    parser.add_argument('--nodeploy', help='do not deploy',
                         action='store_true', default=False)
    parser.add_argument('--serve', help='serve site',
                         action='store_true', default=False)
    parser.add_argument('--init', help="create new site at path",
                         action='store_true', default=False)
    args = parser.parse_args()

    engine = core.Drupan()

    if not vars(args)['init']:
        path = vars(args)['path']
        nodeploy = vars(args)['nodeploy']
        serve = vars(args)['serve']
        engine.setup(path, nodeploy, serve)
        engine.run()
    else:
        engine.initialize(vars(args)['path'])
