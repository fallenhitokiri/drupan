# -*- coding: utf-8 -*-

"""
    drupan.serve

    Serve a generated site locally.
"""

import os
from http.server import SimpleHTTPRequestHandler
from socketserver import TCPServer


class HTTPServer(object):
    """Serve the writer output directory over http."""
    def __init__(self, config):
        """Arguments:
            config: drupan config instance
        """
        self.directory = config.get_option("writer", "directory")
        self.logger = config.logger
        self.port = 9000

    def serve(self):
        cwd = os.getcwd()
        os.chdir(self.directory)

        httpd = TCPServer(("", self.port), SimpleHTTPRequestHandler)
        print( "server running on http://localhost:{0}".format(self.port))
        try:
            self.logger.log(
                "server running on http://localhost:{0}".format(self.port)
            )
            httpd.serve_forever()
        except KeyboardInterrupt:
            self.logger.log("shutting down server\n")

        os.chdir(cwd)
