# -*- coding: utf-8 -*-
import argparse
import sys
import os
import traceback
from .engine import Engine
from .version import __version__

KISS = "Keep it simple, stupid!"
WRONG_VERSION = """
YO!
"""

INIT = """
Les get it!
"""


def cmd():
    """command line entry point"""
    desc = f"{KISS} v{__version__}"
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
        print(INIT)
        sys.exit()

    args = parser.parse_args()

    engine = Engine()
    engine.deployment = None

    # if someone uses a directory as config it is likely a drupan 1 setup
    # point to the migration guide.
    if os.path.isdir(args.config):
        print(WRONG_VERSION)
        sys.exit()

    engine.config.from_file(args.config)
    try:
        engine.prepare_engine()
    except Exception as e:
        print(f"Got Exception {e} \n")
        print(engine.context_info())
        tb = traceback.format_exc()
        print(tb)
        exit(1)

    try:
        engine.run()
    except Exception as e:
        print(f"Got Exception {e} \n")
        print(engine.context_info())
        tb = traceback.format_exc()
        print(tb)
        # exit(1)

    if args.serve:
        engine.serve()
