


## Usage with Cron

Note that `recomi` distinguishes between routine output,
which is sent to stdout,
and errors/warnings,
which are sent to stderr.
Thus you can use a shell pipeline or redirection to send stdout to
a log somewhere while letting cron collect up stderr and send it as
an email:

    8 4 * * * recomi fetch /path/to/dir | logger -t recomi-dir
