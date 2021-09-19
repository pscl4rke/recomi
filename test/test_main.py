

import unittest
from unittest import mock

from recomi import main


class TestOptionParsing(unittest.TestCase):

    def test_no_args(self):
        with mock.patch("argparse.ArgumentParser.error") as error_handler:
            opts = main.parse_args([])
        error_handler.assert_called_once()
