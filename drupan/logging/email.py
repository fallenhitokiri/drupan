# -*- coding: utf-8 -*-
from sender import Mail


CFG_KEY = "logging"
CFG_USER = "user"
CFG_PASSWORD = "password"
CFG_HOST = "host"
CFG_SENDER = "sender"
CFG_TO = "to"
SUBJECT = "drupan output"


class EmailLogger(object):
    def __init__(self, config):
        user = config.get_option(CFG_KEY, CFG_USER, optional=False)
        password = config.get_option(CFG_KEY, CFG_PASSWORD, optional=False)
        host = config.get_option(CFG_KEY, CFG_HOST, optional=False)

        self.to = config.get_option(CFG_KEY, CFG_TO, optional=False)
        self.sender = config.get_option(CFG_KEY, CFG_SENDER, optional=False)
        self.messages = list()
        self.mail = Mail(
            host,
            port=25,
            username=user,
            password=password,
            use_tls=True,
            use_ssl=False,
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
