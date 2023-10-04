

import configparser
import os
import subprocess

from .shared import CmdError

from . import git


def path_to_name(path, onlybase=True):
    if ":" in path:
        ssh_host, colon, path = path.partition(":")
    if onlybase:
        name = os.path.basename(path)
    else:
        name = path.lstrip("/").replace("/", "__")
    if name.endswith(".git"):
        name = name[:-4]
    return name


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

    def clone_not_configured(self):
        if "clone" not in self.config.sections():  # pragma: no cover
            return ["Missing [clone] section"]
        errors = []
        if "list" not in self.config["clone"]:  # pragma: no cover
            errors.append("Missing [clone].list option")
        if "url" not in self.config["clone"]:  # pragma: no cover
            errors.append("Missing [clone].url option")
        return errors

    def local_repos(self):
        for name in sorted(os.listdir(self.base_path)):
            path = os.path.join(self.base_path, name)
            if os.path.isdir(path):
                yield git.LocalGitRepo(path)

    def upstream_list(self):
        cmd = self.config["clone"]["list"]
        try:
            output = subprocess.check_output(cmd, shell=True, cwd=self.base_path)
        except subprocess.CalledProcessError as exc:
            raise CmdError("Exit code %i from %s" % (exc.returncode, cmd))
        return output.decode("ascii").splitlines()

    def url_for(self, name, path):
        pattern = self.config["clone"]["url"]
        return pattern.format(name=name, path=path)

    def upstream_repos(self):
        onlybase = self.config["clone"].getboolean("onlybase", True)
        for path in self.upstream_list():
            name = path_to_name(path, onlybase=onlybase)
            yield git.UpstreamGitRepo(name, self.url_for(name, path), self.repo_type())

    def missing_repos(self):
        local_names = [repo.name for repo in self.local_repos()]
        for repo in self.upstream_repos():
            if repo.name not in local_names:
                yield repo

    def repo_type(self):
        repo_type = self.config["clone"].get("type", "mirror")
        if repo_type not in ("mirror", "mirror-ff", "bare", "working"):
            raise ValueError("Invalid type: %r" % repo_type)  # pragma: no cover
        return repo_type

    def warn_of_new_clone(self):
        return self.config["clone"].getboolean("warn", True)
