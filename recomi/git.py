

import os
import subprocess


class CmdError(Exception):
    pass


class GitRepo:

    def __init__(self, path):
        self.path = path

    def is_a_bare_repo(self):
        if os.path.exists(os.path.join(self.path, ".git")):
            return False
        else:
            return True

    def fetch(self):
        if self.is_a_bare_repo():
            args = ["git", "fetch", "--all"]
        else:
            args = ["git", "pull"]
        return_code = subprocess.call(args, cwd=self.path)
        if return_code != 0:
            raise CmdError("Failed")

    def gc(self):
        args = ["git", "gc"]
        return_code = subprocess.call(args, cwd=self.path)
        if return_code != 0:
            raise CmdError("Failed")
