# -*- coding: utf-8 -*-
import argparse
import sys

from .engine import Engine
from .version import __version__
from .initialize import bootstrap


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
        help="create new site at path",
        action="store_true",
        default=False
    )
    parser.add_argument(
        "--deploy",
        help="deploy without generating the site",
        action="store_true",
        default=False
    )
    args = parser.parse_args()

    if args.init:
        bootstrap(args.config)
        sys.exit()

    engine = Engine()

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
