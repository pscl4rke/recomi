

import os
import unittest

from recomi import collecting


class TestPathToName(unittest.TestCase):

    def test_ordinary(self):
        self.assertEqual(collecting.path_to_name("foo"), "foo")

    def test_bare(self):
        self.assertEqual(collecting.path_to_name("foo.git"), "foo")

    def test_path(self):
        self.assertEqual(collecting.path_to_name("baz/bar/foo.git"), "foo")

    def test_ssh_host_without_path(self):
        self.assertEqual(collecting.path_to_name("bar:foo.git"), "foo")

    def test_ssh_host_and_path(self):
        self.assertEqual(collecting.path_to_name("baz:bar/foo.git"), "foo")

    def test_url(self):
        self.assertEqual(collecting.path_to_name("git://bar/foo.git"), "foo")


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

    def test_url_for(self):
        expected = "https://example.com/foo/bar/reponame.git"
        self.assertEqual(self.collection.url_for("reponame", "zzz/reponame"), expected)

    def test_type(self):
        self.assertEqual(self.collection.repo_type(), "mirror")

    def test_warn_of_new_clone(self):
        self.assertEqual(self.collection.warn_of_new_clone(), True)

    def test_upstream_repos(self):
        repos = list(self.collection.upstream_repos())
        self.assertEqual(len(repos), 3)
        self.assertEqual(repos[0].name, "one")
        self.assertEqual(repos[2].name, "three")
