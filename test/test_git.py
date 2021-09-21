

import unittest

from recomi import git


class TestLocal(unittest.TestCase):

    def test_bare_name(self):
        repo = git.LocalGitRepo("/path/to/repo.git")
        self.assertEqual(repo.name, "repo")

    def test_name(self):
        repo = git.LocalGitRepo("/path/to/repo")
        self.assertEqual(repo.name, "repo")


class TestUpstream(unittest.TestCase):

    def test_upstream(self):
        repo = git.UpstreamGitRepo("foobar")
        self.assertTrue(True)
