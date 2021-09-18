

import unittest

from recomi import git


class TestPlaceholder(unittest.TestCase):

    def test_example(self):
        repo = git.GitRepo("/path/to/repo")
        self.assertTrue(True)
