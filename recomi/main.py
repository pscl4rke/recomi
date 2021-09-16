

import argparse
import os
import sys


class Collection:

    def __init__(self, base_path):
        if not os.path.isdir(base_path):
            return ValueError("Invalid base directory: %r" % base_path)
        self.base_path = base_path

    def repositories(self):
        for name in sorted(os.listdir(self.base_path)):
            path = os.path.join(self.base_path, name)
            if os.path.isdir(path):
                yield path


def handle_fetch(opts):
    for collection in opts.collections:
        print(collection.base_path)
        for repo in collection.repositories():
            print("  Want to fetch in %s" % repo)


def command(value):
    if value == "fetch":
        return handle_fetch
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
