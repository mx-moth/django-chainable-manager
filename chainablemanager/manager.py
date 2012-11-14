from django.db.models import Manager
from django.db.models.query import QuerySet


class ChainableManagerMetaclass(type):
    """
    Metaclass for ChainableManager.
    """
    def __new__(mcs, name, bases, attrs):

        # Get the custom QuertSet mixin defined on the class
        QuerySetMixin = attrs.get('QuerySetMixin', object)

        # Add it as a base to this class
        bases = bases + (QuerySetMixin, )

        # And also as a base to a custom QuerySet
        class FilterQuerySet(QuerySet, QuerySetMixin):
            pass
        FilterQuerySet.__name__ = 'QuerySet'

        # Set the queryset, and a custom get_query_set method
        attrs['QuerySet'] = FilterQuerySet

        # Finish constructing the class
        return super(ChainableManagerMetaclass, mcs).__new__(
            mcs, name, bases, attrs)


class ChainableManager(Manager):
    """
    A Model Manager that allows chaining custom filters and other methods on
    both the manager and any querysets produced by it.

    Add a class named `QuerySetMixin` to the Manager, and define all your
    custom, chainable methods on this class instead.
    """
    __metaclass__ = ChainableManagerMetaclass

    def get_query_set(self):
        """
        Create a QuerySet for querying this model. Will also have all the
        chainable methods defined on `QuerySetMixin`.
        """
        return self.QuerySet(self.model, using=self._db)
