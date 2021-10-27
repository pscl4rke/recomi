

import argparse
import sys
import time

from . import git
from . import collecting
from . import __version__


DESCRIPTION = "Repository Collection Mirror (version %s)" % __version__


def info(msg):
    sys.stdout.write("%s\n" % msg)
    sys.stdout.flush()


def warn(msg):
    if sys.stderr.isatty():
        sys.stderr.write("\033[31;1mWARNING:\033[0m recomi: %s\n" % msg)
    else:
        sys.stderr.write("WARNING: recomi: %s\n" % msg)
    sys.stderr.flush()


class LoopingCommand:

    def __init__(self, fetch=False, gc=False, clone=False):
        self.should_fetch = fetch
        self.should_gc = gc
        self.should_clone = clone

    def run(self, opts):
        start_run = time.time()
        failures = 0
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
                except git.CmdError as exc:
                    warn("%s: %r" % (repo.path, exc))
                    failures = failures + 1
            if self.should_clone:
                errors = collection.clone_not_configured()
                if len(errors) > 0:
                    warn("Invalid configuration for clone: %r" % errors)
                    failures = failures + 1
                    continue
                for repo in collection.missing_repos():
                    try:
                        info("\n[BEGIN clone %s]" % repo.clone_from)
                        if collection.warn_of_new_clone():
                            warn("New repository detected: %s" % repo.clone_from)
                        repo.clone(collection.base_path)
                        info("[END clone]")
                    except git.CmdError as exc:
                        warn("%s: %r" % (repo.clone_from, exc))
                        failures = failures + 1
        duration = time.time() - start_run
        info("\nRecomi finished in %i seconds" % duration)
        if failures:
            warn("==============================")
            warn("Overall there were %i failures" % failures)
            sys.exit(1)


def command(value):
    if value == "fetch":
        return LoopingCommand(fetch=True)
    elif value == "gc":
        return LoopingCommand(gc=True)
    elif value == "clone":
        return LoopingCommand(clone=True)
    elif value == "mirror":
        return LoopingCommand(fetch=True, gc=True, clone=True)
    else:
        raise ValueError("No such command %r" % value)


def parse_args(args):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("command", type=command)
    parser.add_argument("collections", nargs="+", type=collecting.Collection)
    opts = parser.parse_args(args)
    return opts


def main():
    opts = parse_args(sys.argv[1:])
    opts.command.run(opts)


if __name__ == "__main__":
    main()
