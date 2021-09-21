

import configparser
import os
import subprocess

from . import git


class Collection:

    def __init__(self, base_path):
        if not os.path.isdir(base_path):
            raise ValueError("Invalid base directory: %r" % base_path)
        self.base_path = base_path
        self._parse_config()

    def _parse_config(self):
        self.config = configparser.ConfigParser()
        config_path = os.path.join(self.base_path, "recomi.ini")
        if os.path.exists(config_path):
            self.config.read(config_path)

    def local_repos(self):
        for name in sorted(os.listdir(self.base_path)):
            path = os.path.join(self.base_path, name)
            if os.path.isdir(path):
                yield git.LocalGitRepo(path)

    def upstream_list(self):
        cmd = self.config["clone"]["list"]
        output = subprocess.check_output(cmd, shell=True, cwd=self.base_path)
        return output.decode("ascii").splitlines()

    def url_for(self, name):
        pattern = self.config["clone"]["url"]
        return pattern.format(name=name)

    def upstream_repos(self):
        for name in self.upstream_list():
            if name.endswith(".git"):
                name = name[:-4]
            yield git.UpstreamGitRepo(name, self.url_for(name), self.repo_type())

    def missing_repos(self):
        local_names = [repo.name for repo in self.local_repos()]
        for repo in self.upstream_repos():
            if repo.name not in local_names:
                yield repo

    def repo_type(self):
        repo_type = self.config["clone"].get("type", "mirror")
        if repo_type not in ("mirror", "bare", "working"):
            raise ValueError("Invalid type: %r" % repo_type)
        return repo_type

    def warn_of_new_clone(self):
        return self.config["clone"].get("warn", True)
