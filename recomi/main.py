

import argparse
import os
import sys

import git


def info(msg):
    sys.stdout.write("%s\n" % msg)
    sys.stdout.flush()


def warn(msg):
    sys.stderr.write("%s\n" % msg)
    sys.stderr.flush()


class Collection:

    def __init__(self, base_path):
        if not os.path.isdir(base_path):
            return ValueError("Invalid base directory: %r" % base_path)
        self.base_path = base_path

    def repositories(self):
        for name in sorted(os.listdir(self.base_path)):
            path = os.path.join(self.base_path, name)
            if os.path.isdir(path):
                yield git.GitRepo(path)


def for_each_repo(opts, func):
    failures = []
    for collection in opts.collections:
        info("Collection: %s" % collection.base_path)
        for repo in collection.repositories():
            info("Repository: %s" % repo.path)
            try:
                func(opts, repo)
            except git.CmdError:
                warn("Failed: %s" % repo.path)
                failures.append((collection, repo))
    if failures:
        sys.exit(1)


def do_fetch(opts, repo):
    repo.fetch()


def do_gc(opts, repo):
    repo.gc()


def command(value):
    if value == "fetch":
        return lambda opts: for_each_repo(opts, do_fetch)
    elif value == "gc":
        return lambda opts: for_each_repo(opts, do_gc)
    else:
        raise ValueError("No such command %r" % value)


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("command", type=command)
    parser.add_argument("collections", nargs="+", type=Collection)
    opts = parser.parse_args(args)
    return opts


def main():
    opts = parse_args(sys.argv[1:])
    opts.command(opts)


if __name__ == "__main__":
    main()
