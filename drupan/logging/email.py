# -*- coding: utf-8 -*-
from sender import Mail


CFG_KEY = "logging"
CFG_USER = "user"
CFG_PASSWORD = "password"
CFG_HOST = "host"
CFG_SENDER = "sender"
CFG_TO = "to"
CFG_PORT = "port"
CFG_TLS = "tls"
CFG_SSL = "ssl"

DEFAULT_PORT = 587
DEFAULT_TLS = True
DEFAULT_SSL = False

SUBJECT = "drupan output"


class EmailLogger(object):
    def __init__(self, config):
        user = config.get_option(CFG_KEY, CFG_USER)
        password = config.get_option(CFG_KEY, CFG_PASSWORD)
        host = config.get_option(CFG_KEY, CFG_HOST)
        port = config.get_option(CFG_KEY, CFG_PORT, optional=True)\
            or DEFAULT_PORT
        tls = config.get_option(CFG_KEY, CFG_TLS, optional=True) or DEFAULT_TLS
        ssl = config.get_option(CFG_KEY, CFG_SSL, optional=True) or DEFAULT_SSL

        self.to = config.get_option(CFG_KEY, CFG_TO, optional=False)
        self.sender = config.get_option(CFG_KEY, CFG_SENDER, optional=False)
        self.messages = list()
        self.mail = Mail(
            host,
            port=port,
            username=user,
            password=password,
            use_tls=tls,
            use_ssl=ssl,
            debug_level=None
        )

    def log(self, message):
        self.messages.append(message)

    def close(self):
        body = "\n".join(self.messages)
        self.mail.send_message(
            SUBJECT,
            fromaddr=self.sender,
            to=self.to,
            body=body
        )
