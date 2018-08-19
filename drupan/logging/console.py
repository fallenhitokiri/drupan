# -*- coding: utf-8 -*-
import logging


class ConsoleLogger(object):
    def __init__(self, config):
        self.logger = logging.getLogger("drupan")

    def log(self, message):
        self.logger.info(message)

    def close(self):
        pass
