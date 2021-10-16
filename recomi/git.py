

import os
import subprocess


DRY_RUN = os.environ.get("RECOMI_DRY_RUN", "FALSE").lower().startswith("t")


class CmdError(Exception):
    pass


class Repo:

    def _run(self, cwd, args):
        if DRY_RUN:
            print("I would have run %r" % args)
            return
        return_code = subprocess.call(args, cwd=cwd, stderr=subprocess.STDOUT)
        if return_code != 0:
            raise CmdError("Failed")


class LocalGitRepo(Repo):

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
        args = [
            "git",
            "-c", "gc.autoDetach=false",
            "-c", "fetch.fsckObjects=true",
        ]
        if self.is_a_bare_repo():
            args.extend(["fetch", "--all"])
        else:
            args.extend(["pull"])
        self._run(self.path, args)

    def gc(self):
        args = ["git",
                "-c", "gc.autoDetach=false",
                "-c", "gc.auto=1",  # git defaults to 6700
                "gc", "--auto"]
        self._run(self.path, args)


class UpstreamGitRepo(Repo):

    def __init__(self, name, clone_from, repo_type):
        self.name = name
        self.clone_from = clone_from
        self.repo_type = repo_type

    def dest(self):
        if self.repo_type == "working":
            return self.name
        return self.name + ".git"

    def clone_args(self):
        args = ["git", "clone"]
        if self.repo_type == "mirror":
            args.append("--mirror")
        if self.repo_type == "bare":
            args.append("--bare")
        args.append(self.clone_from)
        args.append(self.dest())
        return args

    def clone(self, parent):
        self._run(parent, self.clone_args())
