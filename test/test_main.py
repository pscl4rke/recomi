

import unittest

from recomi import main


class TestCollection(unittest.TestCase):

    def test_absent_collections(self):
        with self.assertRaises(ValueError):
            main.Collection("/path/to/collection/that/doesnt/exist")
