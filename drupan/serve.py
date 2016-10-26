# -*- coding: utf-8 -*-

"""
    drupan.serve

    Serve a generated site locally.
"""

try:
    import SimpleHTTPServer
    import SocketServer
except ImportError:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
import os


def http(directory, port=9000):
    """
    Serve a directory over http.

    Arguments:
        directory: directory of the generated site
        port: port to run the httpd on
    """
    cwd = os.getcwd()
    os.chdir(directory)

    handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", port), handler)

    try:
        print("server running on http://localhost:{0}".format(port))
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("shutting down server\n")

    os.chdir(cwd)
