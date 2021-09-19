

import argparse
import sys

from . import git
from . import collecting


def info(msg):
    sys.stdout.write("%s\n" % msg)
    sys.stdout.flush()


def warn(msg):
    sys.stderr.write("%s\n" % msg)
    sys.stderr.flush()


def for_each_repo(opts, func):
    failures = []
    for collection in opts.collections:
        info("\nCollection: %s" % collection.base_path)
        for repo in collection.repositories():
            info("\nRepository: %s" % repo.path)
            try:
                func(opts, repo)
                info("Done")
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
    parser.add_argument("collections", nargs="+", type=collecting.Collection)
    opts = parser.parse_args(args)
    return opts


def main():
    opts = parse_args(sys.argv[1:])
    opts.command(opts)


if __name__ == "__main__":
    main()
