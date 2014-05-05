# -*- coding: utf-8 -*-
import argparse

from .engine import Engine


def cmd():
    """command line entry point"""
    desc = "drupan v{0}".format(2)
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
    args = parser.parse_args()

    engine = Engine()

    engine.config.from_file(args.config)
    engine.prepare_engine()
    engine.run()

    if args.serve:
        engine.serve()
