# -*- coding: utf-8 -*-

"""
    drupan.serve

    Serve a generated site locally.
"""

import os

try:
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer
except ImportError:
    from http.server import SimpleHTTPRequestHandler
    from socketserver import TCPServer


def server(directory, port=9000):
    """
    Serve a directory over http.

    Arguments:
        directory: directory of the generated site
        port: port to run the httpd on
    """
    cwd = os.getcwd()
    os.chdir(directory)

    httpd = TCPServer(("", port), SimpleHTTPRequestHandler)

    try:
        print("server running on http://localhost:{0}".format(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("shutting down server\n")

    os.chdir(cwd)
