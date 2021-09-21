

import os
import subprocess


class CmdError(Exception):
    pass


class LocalGitRepo:

    def __init__(self, path):
        self.path = path
        self.name = self.work_out_name()

    def work_out_name(self):
        name = os.path.basename(self.path)
        if name.endswith(".git"):
            name = name[:-4]
        return name

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
        return_code = subprocess.call(args, cwd=self.path, stderr=subprocess.STDOUT)
        if return_code != 0:
            raise CmdError("Failed")

    def gc(self):
        args = ["git", "gc"]
        return_code = subprocess.call(args, cwd=self.path, stderr=subprocess.STDOUT)
        if return_code != 0:
            raise CmdError("Failed")


class UpstreamGitRepo:

    def __init__(self, name, clone_from):
        self.name = name
        self.clone_from = clone_from
