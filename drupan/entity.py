# -*- coding: utf-8 -*-
"""
    drupan.entity

    Each page / post / snippet / ... is defined as one entity.
"""

import re
from datetime import datetime


class Entity(object):
    """define an entity and all helper methods"""
    def __init__(self, config):
        self.config = config

        self.meta = dict()
        self.raw = None
        self.content = None

        # store results generated by the matching property
        self._slug = None
        self._url = None
        self._created = None
        self._updated = None

    @property
    def layout(self):
        """
        Returns:
            layout for this entity
        """
        return self.meta["layout"]

    @property
    def url(self):
        """
        Return the URL for this entity. If there is no URL key in the meta
        dictionary config["urls"][layout] will be used.

        Returns:
            url for this entity
        """
        if self._url:
            return self._url

        if "url" in self.meta:
            layout = self.meta["url"]
        else:
            layout = self.config.url_scheme[self.layout]

        for key in layout.split("/"):
            if not len(key) > 0:
                continue

            if not key.startswith("%"):
                continue

            value = self.get_url_value(key)
            layout = layout.replace(key, value)

        if len(layout) > 0 and not layout.endswith("/"):
            layout += "/"

        if len(layout) > 0 and not layout.startswith("/"):
            layout = "/" + layout

        self._url = layout
        return self._url

    @property
    def slug(self):
        """
        Returns:
            slug based on the title
        """
        if self._slug:
            return self._slug

        clean = re.sub('[^A-Za-z0-9]+', '-', self.meta['title'])

        # multiple '-' do not look nice
        clean = clean.replace('----', '-')
        clean = clean.replace('---', '-')
        clean = clean.replace('--', '-')

        # urls should not start or end with a -
        if clean.endswith("-"):
            clean = clean[:-1]

        if clean.startswith("-"):
            clean = clean[1:]

        clean = clean.lower()

        self._slug = clean
        return self._slug

    @property
    def created(self):
        """
        Returns:
            create date and time as datetime instance
        """
        if self._created:
            return self._created

        if "date" in self.meta:
            dt = self.meta["date"]
        else:
            dt = datetime.now()

        self._created = dt

        return self._created

    @property
    def updated(self):
        """
        Returns:
            update date and time as datetime instance
        """
        if self._updated:
            return self._updated

        dt = self.meta.get("updated", None)

        # update timestamp is not required - use the created timestamp
        if not dt:
            self._updated = self.created
            return self._updated

        self._updated = dt
        return self._updated

    @property
    def path(self):
        """
        Returns:
            path without leading or trailing slash
        """
        if self.url.rsplit("/", 1)[0] != "":
            return self.url.rsplit("/", 1)[0].split("/", 1)[1]
        return ""

    def get_url_value(self, key):
        """
        There are three possible scenarios where 'key' can be stored

          - part of the created timestamp
          - in the meta dictionary
          - as attribute of an Entity instance

        Arguments:
            key: key to lookup value for

        Returns:
            variable to be used in the URL for a given key
        """
        key = key[1:]  # remove %

        if hasattr(self.created, key):
            # return as string, not int
            return str(getattr(self.created, key))

        if key in self.meta:
            return self.meta[key]

        return getattr(self, key)
