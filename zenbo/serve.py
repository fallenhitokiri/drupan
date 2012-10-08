# -*- coding: utf-8 -*-

import SimpleHTTPServer
import SocketServer
import os


class Server(object):
    """simple httpd to test your site"""
    def __init__(self, site):
        self.output = site.config.output
        self.site = site
        self.port = 9000

    def serve(self):
        """run server with output directory as server root"""
        cwd = os.getcwd()
        os.chdir(self.output)

        handler = SimpleHTTPServer.SimpleHTTPRequestHandler
        httpd = SocketServer.TCPServer(("", self.port), handler)

        try:
            print "server running on port 9000"
            httpd.serve_forever()
        except KeyboardInterrupt:
            print "shutting down server\n"

        os.chdir(cwd)
