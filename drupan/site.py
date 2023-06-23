from .observer import ConcreteSubject

"""
    drupan.site

    Represent a site holding all information necessary to generate it and
    look up certain entities.
"""

from datetime import datetime


def search(entity, key, value):
    """
    Arguments:
        entity: drupan.Entity
        key: key to use
        value: value to match

    Returns:
        True if an entity has a attribute or key in meta with value as
        value
    """
    # TODO: comparison should be more flexible
    if key in entity.meta:
        if entity.meta[key] == value:
            return True

    if hasattr(entity, key):
        if getattr(entity, key) == value:
            return True

    return False


class Site(ConcreteSubject):
    dont_overwrite = ['entities', 'date', 'templates', 'assets', 'images']

    def __init__(self, **kwargs):
        self.entities = list()  # list for drupan.entity.Entity
        self.date = datetime.now()
        self.templates = dict()
        self.assets = dict()
        self.images = dict()
        self.__dict__.update((k, v) for k, v in kwargs.items() if k not in self.dont_overwrite)
        self.context_name = kwargs.get('site_name', 'ReedSite')
        self.site_wide = {

        }

    def get(self, key, value):
        """
        Filter entities and return one or more entities with a key that
        matches a given value.

        Arguments:
            key: key to look up - either a key in meta or attribute
            value: value to match

        Returns:
            Entity() or list with Entity()s
        """
        results = list()

        for entity in self.entities:
            self.notify(f"checking {entity} for search")
            if search(entity, key, value):
                results.append(entity)

        if len(results) > 1:
            return results
        elif len(results) == 1:
            return results[0]

        return None
