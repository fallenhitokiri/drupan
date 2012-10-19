#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""drupan executable"""

import argparse

from drupan import core


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='drupan')
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
        
