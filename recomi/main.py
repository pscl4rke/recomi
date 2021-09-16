

import argparse
import os
import sys

import git


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
        print(collection.base_path)
        for repo in collection.repositories():
            try:
                func(opts, repo)
            except git.CmdError:
                failures.append((collection, repo))
    for collection, repo in failures:
        print("Failed: %s" % repo.path)
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