#! /usr/bin/env python
from plumbum import cli, RETCODE
from plumbum.cmd import (
    supervisord, flake8, echo, nc, uwsgi, flask
)


class AppMain(cli.Application):

    def main(self, *args):
        if args:
            print("Unknown command {0!r}".format(args[0]))
            return 1  # error exit code
        if not self.nested_command:
            print("No command given")
            return 1  # error exit code


@AppMain.subcommand('server')
class AppServer(cli.Application):

    def main(self):
        return supervisord['-n'] & RETCODE(FG=True)


@AppMain.subcommand('worker')
class AppWorker(cli.Application):

    def main(self):
        return supervisord[
                   '-n', '-c', '/etc/supervisor/celery-worker.supervisord.conf'
        ] & RETCODE(FG=True)


@AppMain.subcommand('zmqrpc')
class AppRpcserver(cli.Application):

    def main(self):
        return supervisord[
                   '-n', '-c', '/etc/supervisor/zmqrpc.supervisord.conf'
               ] & RETCODE(FG=True)


if __name__ == '__main__':
    AppMain.run()
