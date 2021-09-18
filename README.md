
# Recomi -- The Repository Collection Mirror

Batch-orientated tool for keeping local collections of git repositories
mirroring their remote upstream counterparts.

Each "collection" is a directory that contains repositories.
Normally the repositories would be `--mirror` ones,
but this works with ordinary clones too.

Currently this tool is little more than `git fetch` in a `for` loop.
But in time it will gain capabilities for detecting new repos becoming
available upsream and automatically cloning them.
(Famous last words!)

## Usage

    $ recomi fetch /path/to/collection1 /path/to/collection2...
    $ recomi gc /path/to/collection1 /path/to/collection2...

## Installation

    $ pip install git+https://github.com/pscl4rke/recomi.git

## Usage with Cron

Note that `recomi` distinguishes between routine output,
which is sent to stdout,
and errors/warnings,
which are sent to stderr.
Thus you can use a shell pipeline or redirection to send stdout to
a log somewhere while letting cron collect up stderr and send it as
an email:

    8 4 * * * recomi fetch /path/to/dir | logger -t recomi-dir

## Licence

This software is licensed under the GPLv3.
