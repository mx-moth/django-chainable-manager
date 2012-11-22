from functools import wraps

from django.db.models import Manager
from django.db.models.query import QuerySet


def _make_proxy(name, fn):
    @wraps(fn)
    def _proxy(self, *args, **kwargs):
        qs = self.get_query_set()
        return getattr(qs, name)(*args, **kwargs)

    return _proxy


class ChainableManagerMetaclass(type):
    """
    Metaclass for ChainableManager.
    """
    def __new__(cls, name, bases, attrs):
        cls = super(ChainableManagerMetaclass, cls).__new__(
            cls, name, bases, attrs)

        # Get the custom QuertSet mixin defined on the class
        QuerySetMixin = getattr(cls, 'QuerySetMixin', None)

        # Bail here if there is no QuerySetMixin
        if QuerySetMixin is None:
            return cls

        # Make a custom QuerySet from the mixin
        methods = dict(QuerySetMixin.__dict__)
        ChainableQuerySet = type('ChainableQuerySet', (QuerySet, ),
            methods)
        setattr(cls, 'ChainableQuerySet', ChainableQuerySet)

        # Make a proxy for all of the methods on the mixin
        for name, fn in methods.items():
            if callable(fn):
                setattr(cls, name, _make_proxy(name, fn))

        return cls


class ChainableManager(Manager):
    """
    A Model Manager that allows chaining custom filters and other methods on
    both the manager and any querysets produced by it.

    Add a class named `QuerySetMixin` to the Manager, and define all your
    custom, chainable methods on this class instead.
    """
    __metaclass__ = ChainableManagerMetaclass

    use_for_related_fields = True

    def get_query_set(self):
        """
        Create a QuerySet for querying this model. Will also have all the
        chainable methods defined on `QuerySetMixin`.
        """
        return self.ChainableQuerySet(self.model, using=self._db)
