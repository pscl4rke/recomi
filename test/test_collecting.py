

import os
import unittest

from recomi import collecting


class TestMissingCollection(unittest.TestCase):

    def test_cannot_be_instantiated(self):
        with self.assertRaises(ValueError):
            collecting.Collection("/path/to/collection/that/doesnt/exist")


class TestDummyCollectionWithConfig(unittest.TestCase):

    def setUp(self):
        dummy = os.path.join(os.path.dirname(__file__), "DummyCollection")
        self.collection = collecting.Collection(dummy)

    def test_upstream_list(self):
        names = self.collection.upstream_list()
        self.assertEqual(names, ["one", "two", "three"])

    def test_upstream_repos(self):
        repos = list(self.collection.upstream_repos())
        self.assertEqual(len(repos), 3)
        self.assertEqual(repos[0].name, "one")
        self.assertEqual(repos[2].name, "three")
