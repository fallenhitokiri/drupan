#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Zenbo executable"""

import argparse

from core import Zenbo


def main():
    """Main"""
    engine = Zenbo()
    engine.run()


if __name__ == '__main__':
    main()
