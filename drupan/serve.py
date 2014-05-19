# -*- coding: utf-8 -*-

"""
    drupan.serve

    Serve a generated site locally.
"""

import SimpleHTTPServer
import SocketServer
import os


def http(dir, port=9000):
    """
    Serve a directory over http.

    Arguments:
        dir: directory of the generated site
        port: port to run the httpd on
    """
    cwd = os.getcwd()
    os.chdir(dir)

    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), handler)

    try:
        print "server running on http://localhost:{0}".format(port)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print "shutting down server\n"

    os.chdir(cwd)
