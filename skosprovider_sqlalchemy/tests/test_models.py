import unittest

from . import engine

from sqlalchemy.orm import sessionmaker

class ModelTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = engine

    def setUp(self):
        connection = self.engine.connect()
        self.trans = connection.begin()

        # Setting up SQLAlchemy
        from skosprovider_sqlalchemy.models import Base
        Base.metadata.bind = engine
        sm = sessionmaker(bind=engine)
        self.session= sm()

    def tearDown(self):
        self.session.close()
        self.trans.rollback()


class ConceptTests(ModelTestCase):

    def _get_target_class(self):
        from ..models import Concept
        return Concept

    def test_simple(self):
        from ..models import Label
        l = Label('prefLabel', 'en', 'Churches')
        c = self._get_target_class()(
            id=1,
            labels=[l]
        )
        self.assertEqual(1, c.id)
        self.assertEqual(l, c.label())


class ConceptSchemeTests(ModelTestCase):

    def _get_target_class(self):
        from ..models import ConceptScheme
        return ConceptScheme

    def test_simple(self):
        from ..models import Label
        l = Label('prefLabel', 'en', 'Heritage types')
        c = self._get_target_class()(
            id=1,
            labels=[l]
        )
        self.session.flush()
        self.assertEqual(1, c.id)
        self.assertEqual(l, c.label())


class CollectionTests(ModelTestCase):

    def _get_target_class(self):
        from ..models import Collection
        return Collection

    def _get_concept(self):
        from ..models import Concept, Label
        return Concept(
            id=2,
            labels=[Label('prefLabel', 'en', 'Cathedrals')]
        )

    def test_simple(self):
        from ..models import Label
        l = Label('prefLabel', 'en', 'Churches by function')
        c = self._get_target_class()(
            id=1,
            labels=[l]
        )
        self.assertEqual(1, c.id)
        self.assertEqual(l, c.label())

    def test_members(self):
        col = self._get_target_class()(
            id=1
        )
        c = self._get_concept()
        col.concepts.append(c)
        self.session.flush()
        self.assertEqual(1, len(c.collections))
        self.assertEqual(col, c.collections[0])

