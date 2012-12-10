import datetime

from django.db import models
from django.db.models.query import QuerySet
from django.test import TestCase

from chainablemanager import ChainableManager


class BookManager(ChainableManager):
    class QuerySetMixin:

        def published_in(self, year):
            return self.filter(year=year)

        def in_genre(self, genre):
            return self.filter(genre=genre)


class Author(models.Model):
    name = models.CharField(max_length=255)


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name='books')
    genre = models.CharField(max_length=255)
    year = models.IntegerField()

    objects = BookManager()


def populate_books():
    mieville = Author.objects.create(name='China Mieville')
    banks = Author.objects.create(name='Iain Banks')

    mieville.books.create(name="The City & the City", genre="Crime", year=2009)
    mieville.books.create(name="Kraken", genre="Fantasy", year=2010)
    mieville.books.create(name="Embassytown", genre="Sci Fi", year=2011)
    mieville.books.create(name="Railsea", genre="Fantasy", year=2012)

    # To be pedantic, his Sci Fi works are published under  Iain M. Banks
    banks.books.create(name="The Business", genre="Fantasy", year=1999)
    banks.books.create(name="Dead Air", genre="Fantasy", year=2002)
    banks.books.create(name="The Algebraist", genre="Sci Fi", year=2004)
    banks.books.create(name="Matter", genre="Sci Fi", year=2008)
    banks.books.create(name="The Hydrogen Sonata", genre="Sci Fi", year=2012)
    banks.books.create(name="Stonemouth", genre="Fantasy", year=2012)


class ChainableManagerTests(TestCase):

    def setUp(self):
        populate_books()

    def test_simple_chain(self):

        railsea = Book.objects.get(name="Railsea")
        hydrogen_sonata = Book.objects.get(name="The Hydrogen Sonata")
        stonemouth = Book.objects.get(name="Stonemouth")

        self.assertTrue(hasattr(Book.objects, 'published_in'),
            "Model Manager has chainable method")
        self.assertTrue(callable(Book.objects.published_in),
            "Model Manager has callable chained method")

        books_2012 = Book.objects.published_in(2012)

        self.assertTrue(hasattr(books_2012, 'in_genre'),
            "QuerySet has chainable method")
        self.assertTrue(callable(books_2012.in_genre),
            "QuerySet has callable chained method")

        self.assertEqual(books_2012.count(), 3,
            "Three books published in 2012")
        self.assertEqual(
            set(books_2012), set([railsea, hydrogen_sonata, stonemouth]),
            "Got the correct three books")

        scifi_books_2012 = books_2012.in_genre('Sci Fi')

        self.assertEqual(scifi_books_2012.count(), 1,
            "One sci fi book published in 2012")
        self.assertEqual(
            set(scifi_books_2012), set([hydrogen_sonata]),
            "Got the correct book")

    def test_related_queries(self):
        mieville = Author.objects.get(name='China Mieville')
        banks = Author.objects.get(name='Iain Banks')

        hydrogen_sonata = Book.objects.get(name="The Hydrogen Sonata")
        stonemouth = Book.objects.get(name="Stonemouth")

        mievilles_books = mieville.books
        banks_books = banks.books

        self.assertTrue(hasattr(mievilles_books, 'published_in'),
            "Related Model Manager has chainable method")
        self.assertTrue(callable(mievilles_books.published_in),
            "Related Model Manager has callable chained method")

        self.assertEqual(mievilles_books.count(), 4,
            "We have the correct number of books")
        self.assertEqual(
            set(banks_books.published_in(2012)),
            set([hydrogen_sonata, stonemouth]),
            "Can access first chained method on related manager")
        self.assertEqual(
            set(banks_books.published_in(2012).in_genre("Fantasy")),
            set([stonemouth]),
            "Can access second chained method on related manager")

    def test_correct_classes(self):

        manager = Book.objects

        self.assertIsInstance(manager, models.Manager,
            "Manager should be an instance of models.Manager")
        self.assertIsInstance(manager, ChainableManager,
            "Manager should be an instance of ChainableManager")
        self.assertIsInstance(manager, manager.QuerySetMixin,
            "Manager should be an instance of its QuerySetMixin")

        queryset = manager.all()

        self.assertIsInstance(queryset, QuerySet,
            "QuerySet should be an instance of QuerySet")
        self.assertIsInstance(queryset, manager.ChainableQuerySet,
            "QuerySet should be an instance of manager.ChainableQuerySet")
        self.assertIsInstance(queryset, manager.QuerySetMixin,
            "QuerySet should be an instance of its QuerySetMixin")

    def test_correct_related_classes(self):

        manager = Book.objects

        mieville = Author.objects.get(name='China Mieville')
        mievilles_books = mieville.books

        self.assertIsInstance(mievilles_books, models.Manager,
            "Related manager should be an isntance of models.Manager")
        self.assertIsInstance(mievilles_books, ChainableManager,
            "Related manager should be an instance of manager.ChainableQuerySet")
        self.assertIsInstance(mievilles_books, manager.QuerySetMixin,
            "Related manager should be an instance of its QuerySetMixin")

        queryset = mievilles_books.all()

        self.assertIsInstance(queryset, QuerySet,
            "Related QuerySet should be an instance of QuerySet")
        self.assertIsInstance(queryset, manager.QuerySetMixin,
            "Related QuerySet should be an instance of its QuerySetMixin")
