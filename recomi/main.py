

import argparse
import sys
import time

from .shared import CmdError

from . import collecting


def version():
    versions = []
    # One type of version comes from __version__ embedded into the codebase.
    # It works, but it has to be kept synchronised with the metadata files and
    # the VCS tags.
    try:
        from . import __version__
        versions.append(("embedded", __version__))
    except Exception:
        versions.append(("embedded", None))
    # Another type of version is looked up with importlib, but was only added
    # provisionally in Python 3.8 and accepted in 3.10.
    try:
        from importlib.metadata import version
        versions.append(("distributed", version("recomi")))
    except Exception:
        versions.append(("distributed", None))
    return ", ".join("%s=%r" % (k, v) for (k, v) in versions)


DESCRIPTION = "Repository Collection Mirror (version: %s)" % version()


def info(msg):  # pragma: no cover
    sys.stdout.write("%s\n" % msg)
    sys.stdout.flush()


def warn(msg):  # pragma: no cover
    if sys.stderr.isatty():
        sys.stderr.write("\033[31;1mWARNING:\033[0m recomi: %s\n" % msg)
    else:
        sys.stderr.write("WARNING: recomi: %s\n" % msg)
    sys.stderr.flush()


class LoopingCommand:

    def __init__(self, fetch=False, gc=False, fsck=False, clone=False):
        self.should_fetch = fetch
        self.should_gc = gc
        self.should_fsck = fsck
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
                    if self.should_fsck:
                        info("\n[BEGIN fsck %s]" % repo.path)
                        repo.fsck()
                        info("[END fsck]")
                except CmdError as exc:
                    warn("%s: %r" % (repo.path, exc))
                    failures = failures + 1
            if self.should_clone:
                errors = collection.clone_not_configured()
                if len(errors) > 0:
                    warn("Invalid configuration for clone: %r" % errors)
                    failures = failures + 1
                    continue
                try:
                    missing_repos = list(collection.missing_repos())
                except CmdError as exc:
                    warn("list: %r" % exc)
                    failures = failures + 1
                    break
                for repo in missing_repos:
                    try:
                        info("\n[BEGIN clone %s]" % repo.clone_from)
                        if collection.warn_of_new_clone():
                            warn("New repository detected: %s" % repo.clone_from)
                        repo.clone(collection.base_path)
                        info("[END clone]")
                    except CmdError as exc:
                        warn("%s: %r" % (repo.clone_from, exc))
                        failures = failures + 1
        duration = time.time() - start_run
        info("\nRecomi finished in %i seconds" % duration)
        if failures:
            warn("================================")
            if failures == 1:
                warn("Overall there was %i failure" % failures)
            else:
                warn("Overall there were %i failures" % failures)
            sys.exit(1)


def command(value):
    """Available commands: fetch, gc, fsck, clone, mirror"""
    # Keep the docstring above up-to-date: it's used in help messages
    if value == "fetch":
        return LoopingCommand(fetch=True)
    elif value == "gc":
        return LoopingCommand(gc=True)
    elif value == "fsck":
        return LoopingCommand(fsck=True)
    elif value == "clone":
        return LoopingCommand(clone=True)
    elif value == "mirror":
        return LoopingCommand(fetch=True, gc=True, clone=True)
    else:
        raise ValueError("No such command %r" % value)


def parse_args(args):
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.version = version()
    parser.add_argument("-V", "--version", action="version")
    parser.add_argument("command", type=command, help=command.__doc__)
    parser.add_argument("collections", nargs="+", type=collecting.Collection)
    opts = parser.parse_args(args)
    return opts


def main():  # pragma: no cover
    opts = parse_args(sys.argv[1:])
    try:
        opts.command.run(opts)
    except KeyboardInterrupt:  # Ctrl-C (SigInt)
        warn("Interrupted")


if __name__ == "__main__":  # pragma: no cover
    main()
