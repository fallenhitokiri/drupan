# -*- coding: utf-8 -*-


class NoopLogger(object):
    def log(self, message):
        pass

    def close(self):
        pass
