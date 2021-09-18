

import unittest

from recomi import git


class TestPlaceholder(unittest.TestCase):

    # Mostly all this test suite can do is check for syntax errors

    def test_example(self):
        repo = git.GitRepo("/path/to/repo")
        self.assertTrue(True)
