from functools import wraps

from django.db.models import Manager
from django.db.models.query import QuerySet
from django.utils.six import with_metaclass


def _make_proxy(name, fn):
    @wraps(fn)
    def _proxy(self, *args, **kwargs):
        qs = self.get_queryset()
        return getattr(qs, name)(*args, **kwargs)

    return _proxy


class ChainableManagerMetaclass(type(Manager)):
    """
    Metaclass for ChainableManager.
    """
    def __new__(cls, name, bases, attrs):
        # Construct the class as normal so we can examine it. We will not
        # actually use this class, unless there is no queryset mixin
        temp_cls = super(ChainableManagerMetaclass, cls).__new__(
            cls, name, bases, attrs)

        # Get the custom QuerySet mixin defined on the class
        QuerySetMixin = getattr(temp_cls, 'QuerySetMixin', None)

        # Bail here if there is no QuerySetMixin
        if QuerySetMixin is None:
            return temp_cls

        # Make a custom QuerySet from the mixin
        ChainableQuerySet = type(
            'ChainableQuerySet', (QuerySetMixin, QuerySet), {})

        # Make a new class with the mixin in place
        attrs['ChainableQuerySet'] = ChainableQuerySet
        bases = bases + (QuerySetMixin, )

        cls = super(ChainableManagerMetaclass, cls).__new__(
            cls, name, bases, attrs)

        return cls


class ChainableManager(with_metaclass(ChainableManagerMetaclass, Manager)):
    """
    A Model Manager that allows chaining custom filters and other methods on
    both the manager and any querysets produced by it.

    Add a class named `QuerySetMixin` to the Manager, and define all your
    custom, chainable methods on this class instead.
    """

    use_for_related_fields = True

    def get_queryset(self):
        """
        Create a QuerySet for querying this model. Will also have all the
        chainable methods defined on `QuerySetMixin`.
        """
        return self.ChainableQuerySet(self.model, using=self._db)
