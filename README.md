
# Recomi -- The Repository Collection Mirror

Batch-orientated tool for keeping local collections of git repositories
mirroring their remote upstream counterparts.

Each "collection" is a directory that contains repositories.
Normally the repositories would be `--mirror` ones,
but this works with ordinary clones too.

At its simplest this tool is little more than `git fetch` in a `for` loop.
But what it also offers is a structured way to find out if there are any
new repositories upstream and then automatically clone them.

## Usage

    $ recomi fetch /path/to/collection1 /path/to/collection2...
    $ recomi gc /path/to/collection1 /path/to/collection2...
    $ recomi clone /path/to/collection1 /path/to/collection2...
    $ recomi mirror /path/to/collection1 /path/to/collection2...

The `mirror` command is equivalent to running `fetch` then `gc` then
`clone` for each collection.

## Installation

    $ pip install git+https://github.com/pscl4rke/recomi.git

## Configuration

The `fetch` and `gc` commands need no configuration.

For `clone` you need to create a config file inside each collection
with the name `recomi.ini`.
The bare minimum contents is:

    [clone]
    list = shell-command argument1 argument2...
    url = git://example.com/example/{name}.git

Use `list` to define a shell command that will communicate with the upstream
source and return a list of repositories (one per line).

Use `url` to turn each listed repository into a clonable SSH/URL pattern.
It will replace `{path}` with the full path that `list` returned,
and will replace `{name}` with just the name part.

Also use `type` set to either `working`, `mirror` or `bare` to describe
what type of clone to make.
It is optional and defaults to `mirror`.

By default recomi will warn you (on stderr) when it clones a new repository.
Set `warn` to false to clone without a warning.

Another example:

    [clone]
    list = ssh mygithost list | grep -v bigrepo
    url = mygithost:{name}.git
    type = working

## Usage with Cron

Note that `recomi` distinguishes between routine output,
which is sent to stdout,
and errors/warnings,
which are sent to stderr.
Thus you can use a shell pipeline or redirection to send stdout to
a log somewhere while letting cron collect up stderr and send it as
an email:

    8 4 * * * recomi fetch /path/to/dir | logger -t recomi-dir

## Limitations

* Recomi is deliberately only interested in pulling from upstream repositories
in an unattended manner.
If you would like interactive tooling to manage both pulling and pushing repositories
then look into whether
[myrepos](https://myrepos.branchable.com/)
or [gitbatch](https://github.com/isacikgoz/gitbatch)
might be better suited to you.
* Recomi currently doesn't handle submodules.
* Recomi is vulnerable to forced updates.
Because the default `--mirror` clone leaves `remote.origin.fetch` set to `+refs/*:refs/*`
(with a plus sign at the front)
it will warn but not block history rewriting.
Removing the plus from the refspec is a solution.
The practicality of this is uncertain.

## Debugging

By running `make dev` you can create a development virtualenv,
and can run `./dev/venv/bin/recomi` to test out the program.

By setting the environment variable `RECOMI_DRY_RUN=True` you can see which
`git` commands would have been run without actually running them.

## Licence

This software is licensed under the GPLv3.
