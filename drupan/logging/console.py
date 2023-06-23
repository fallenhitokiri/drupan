# -*- coding: utf-8 -*-
import logging


class ConsoleLogger(object):
    def __init__(self):
        self.logger = logging.getLogger("fluffy")

    def log(self, message):
        self.logger.info(message)

    def close(self):
        pass
