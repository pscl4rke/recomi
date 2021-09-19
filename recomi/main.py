

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


class LoopingCommand:

    def __init__(self, fetch=False, gc=False):
        self.should_fetch = fetch
        self.should_gc = gc

    def run(self, opts):
        failures = []
        for collection in opts.collections:
            info("\nCollection: %s" % collection.base_path)
            for repo in collection.repositories():
                info("\nRepository: %s" % repo.path)
                try:
                    if self.should_fetch:
                        repo.fetch()
                    if self.should_gc:
                        repo.gc()
                    info("Done")
                except git.CmdError:
                    warn("Failed: %s" % repo.path)
                    failures.append((collection, repo))
        if failures:
            sys.exit(1)


def command(value):
    if value == "fetch":
        return LoopingCommand(fetch=True)
    elif value == "gc":
        return LoopingCommand(gc=True)
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
