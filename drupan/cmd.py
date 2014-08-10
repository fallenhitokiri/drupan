# -*- coding: utf-8 -*-
import argparse
import sys
import os

from .engine import Engine
from .version import __version__


WRONG_VERSION = """Your config parameter is a directory. If you just updated
drupan your site is likely still configured for drupan 1, you are using
drupan 2.
Please check the migration guide in the docs directory on
<https://github.com/fallenhitokiri/drupan/docs/migration_1_to_2.md>
"""

INIT = """For a new site you can clone \
<https://github.com/fallenhitokiri/drupan-template-blog> \
which should give you a good starting point and should always be up to date \
with the latest chages.

After cloning switch to the directory and run `drupan config.yaml --serve`
"""


def cmd():
    """command line entry point"""
    desc = "drupan v{0}".format(__version__)
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("config", help="configuration file")
    parser.add_argument(
        "--nodeploy", help="do not deploy", action="store_true", default=False
    )
    parser.add_argument(
        "--serve", help="serve site", action="store_true", default=False
    )
    parser.add_argument(
        "--init",
        help="show how to setup a new site",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--deploy",
        help="deploy without generating the site",
        action="store_true",
        default=False
    )

    if "--init" in sys.argv:
        print INIT
        sys.exit()

    args = parser.parse_args()

    engine = Engine()

    # if someone uses a directory as config it is likely a drupan 1 setup
    # point to the migration guide.
    if os.path.isdir(args.config):
        print WRONG_VERSION
        sys.exit()

    engine.config.from_file(args.config)
    engine.prepare_engine()

    if args.deploy:
        engine.deploy()
        sys.exit()

    engine.run()

    if args.serve:
        engine.serve()

    if not args.nodeploy:
        engine.deploy()
