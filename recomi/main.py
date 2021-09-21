

import argparse
import sys

from . import git
from . import collecting


def info(msg):
    sys.stdout.write("%s\n" % msg)
    sys.stdout.flush()


def warn(msg):
    sys.stderr.write("WARNING: recomi: %s\n" % msg)
    sys.stderr.flush()


class LoopingCommand:

    def __init__(self, fetch=False, gc=False, clone=False):
        self.should_fetch = fetch
        self.should_gc = gc
        self.should_clone = clone

    def run(self, opts):
        failures = []
        for collection in opts.collections:
            info("\nCollection: %s" % collection.base_path)
            for repo in collection.local_repos():
                try:
                    if self.should_fetch:
                        info("\n[BEGIN fetch %s]" % repo.path)
                        repo.fetch()
                        info("[END fetch]")
                    if self.should_gc:
                        info("\n[BEGIN gc %s]" % repo.path)
                        repo.gc()
                        info("[END gc]")
                except git.CmdError:
                    warn("Failed: %s" % repo.path)
                    failures.append((collection, repo))
            if self.should_clone:
                for repo in collection.missing_repos():
                    warn("I cannot clone %r" % repo.name)
        if failures:
            sys.exit(1)


def command(value):
    if value == "fetch":
        return LoopingCommand(fetch=True)
    elif value == "gc":
        return LoopingCommand(gc=True)
    elif value == "clone":
        return LoopingCommand(clone=True)
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
    opts.command.run(opts)


if __name__ == "__main__":
    main()
