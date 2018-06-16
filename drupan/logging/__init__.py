# -*- coding: utf-8 -*-
from drupan.logging.console import ConsoleLogger
from drupan.logging.email import EmailLogger
from drupan.logging.not_found_exception import LoggerNotFoundException


def get_logger(config, name):
    if name == "console":
        return ConsoleLogger(config)
    if name == "email":
        return EmailLogger(config)

    raise LoggerNotFoundException
