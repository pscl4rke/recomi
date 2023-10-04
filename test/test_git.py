

import unittest

from recomi import git, shared


class TestBase(unittest.TestCase):

    def test_running_good(self):
        repo = git.Repo()
        repo._run(".", ["/bin/true"])

    def test_running_bad(self):
        repo = git.Repo()
        with self.assertRaises(shared.CmdError):
            repo._run(".", ["/bin/false"])

    def test_running_invalid_directory(self):
        repo = git.Repo()
        with self.assertRaises(shared.CmdError):
            repo._run("/i/do/not/exist", ["/bin/true"])


class TestLocal(unittest.TestCase):

    def test_bare_name(self):
        repo = git.LocalGitRepo("/path/to/repo.git")
        self.assertEqual(repo.name, "repo")

    def test_name(self):
        repo = git.LocalGitRepo("/path/to/repo")
        self.assertEqual(repo.name, "repo")


class TestUpstream(unittest.TestCase):

    def test_dest_for_default_repo(self):
        repo = git.UpstreamGitRepo("foobar", "host:user/foobar.git", "mirror")
        self.assertEqual(repo.dest(), "foobar.git")

    def test_dest_for_working_repo(self):
        repo = git.UpstreamGitRepo("foobar", "host:user/foobar.git", "working")
        self.assertEqual(repo.dest(), "foobar")
