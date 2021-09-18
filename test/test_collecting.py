

import unittest

from recomi import collecting


class TestMissingCollection(unittest.TestCase):

    def test_cannot_be_instantiated(self):
        with self.assertRaises(ValueError):
            collecting.Collection("/path/to/collection/that/doesnt/exist")
