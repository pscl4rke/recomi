

import os

from . import git


class Collection:

    def __init__(self, base_path):
        if not os.path.isdir(base_path):
            raise ValueError("Invalid base directory: %r" % base_path)
        self.base_path = base_path

    def repositories(self):
        for name in sorted(os.listdir(self.base_path)):
            path = os.path.join(self.base_path, name)
            if os.path.isdir(path):
                yield git.GitRepo(path)
