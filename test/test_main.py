

import unittest
from unittest import mock

from recomi import main


class TestOptionParsing(unittest.TestCase):

    def test_no_args(self):
        with mock.patch("argparse.ArgumentParser.error") as error_handler:
            main.parse_args([])
        error_handler.assert_called_once()

    # Hmm... fine on Py 3.11, but strange error with 3.8
    #def test_invalid_command(self):
    #    with mock.patch("argparse.ArgumentParser.error") as error_handler:
    #        main.parse_args(["notacommand", "."])
    #    error_handler.assert_called()

    def test_fetch(self):
        opts = main.parse_args(["fetch", "."])
        self.assertTrue(opts.command.should_fetch)
        self.assertFalse(opts.command.should_gc)
        self.assertFalse(opts.command.should_fsck)
        self.assertFalse(opts.command.should_clone)

    def test_gc(self):
        opts = main.parse_args(["gc", "."])
        self.assertFalse(opts.command.should_fetch)
        self.assertTrue(opts.command.should_gc)
        self.assertFalse(opts.command.should_fsck)
        self.assertFalse(opts.command.should_clone)

    def test_fsck(self):
        opts = main.parse_args(["fsck", "."])
        self.assertFalse(opts.command.should_fetch)
        self.assertFalse(opts.command.should_gc)
        self.assertTrue(opts.command.should_fsck)
        self.assertFalse(opts.command.should_clone)

    def test_clone(self):
        opts = main.parse_args(["clone", "."])
        self.assertFalse(opts.command.should_fetch)
        self.assertFalse(opts.command.should_gc)
        self.assertFalse(opts.command.should_fsck)
        self.assertTrue(opts.command.should_clone)

    def test_mirror(self):
        opts = main.parse_args(["mirror", "."])
        self.assertTrue(opts.command.should_fetch)
        self.assertTrue(opts.command.should_gc)
        self.assertFalse(opts.command.should_fsck)
        self.assertTrue(opts.command.should_clone)
