# -*- coding: utf-8 -*-
from drupan.logging.console import ConsoleLogger
from drupan.logging.email import EmailLogger
from drupan.logging.noop import NoopLogger


def get_logger(config, name):
    if name == "noop":
        return NoopLogger()
    if name == "email":
        return EmailLogger(config)

    return ConsoleLogger(config)
