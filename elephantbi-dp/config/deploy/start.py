#! /usr/bin/env python
import os
import time

from plumbum import cli, FG, TF, RETCODE, local
from plumbum.cmd import (supervisord, flake8, nosetests, echo, nc, uwsgi, flask,
                         pybabel)


class AppMain(cli.Application):

    def main(self, *args):
        if args:
            print("Unknown command {0!r}".format(args[0]))
            return 1  # error exit code
        if not self.nested_command:
            # will be ``None`` if no sub-command follows
            print("No command given")
            return 1  # error exit code


@AppMain.subcommand('server')
class AppServer(cli.Application):

    def wait_postgres(self):
        postgres_host = os.getenv('DB_ENV_POSTGRES_HOST')
        postgres_port = os.getenv('DB_ENV_POSTGRES_PORT')
        message = ('"Trying connect postgres {0}:{1}"'
                   .format(postgres_host, postgres_port))
        echo[message] & FG
        while not nc['-w', 2, '-z', postgres_host, postgres_port] & TF(FG=True):
            waiting_message = 'Waiting Postgres...'
            echo[waiting_message] & FG
            time.sleep(1)

    def main(self):
        self.wait_postgres()
        return supervisord['-n'] & RETCODE(FG=True)


@AppMain.subcommand('worker')
class AppWorker(cli.Application):

    def wait_postgres(self):
        postgres_host = os.getenv('DB_ENV_POSTGRES_HOST')
        postgres_port = os.getenv('DB_ENV_POSTGRES_PORT')
        message = ('"Trying connect postgres {0}:{1}"'
                   .format(postgres_host, postgres_port))
        echo[message] & FG
        while not nc['-w', 2, '-z', postgres_host, postgres_port] & TF(FG=True):
            waiting_message = 'Waiting Postgres...'
            echo[waiting_message] & FG
            time.sleep(1)

    def main(self):
        self.wait_postgres()
        return supervisord[
                   '-n', '-c', '/etc/supervisor/celery-worker.supervisord.conf'
               ] & RETCODE(FG=True)


@AppMain.subcommand('tests')
class AppTests(cli.Application):

    def main(self):
        nosetests & RETCODE(FG=True)


@AppMain.subcommand('lint')
class AppLint(cli.Application):

    def main(self):
        return flake8['./flexbi', './deploy'] & RETCODE(FG=True)


@AppMain.subcommand('idle')
class AppIdle(cli.Application):

    def main(self):
        while True:
            echo['sleeping...'] & FG
            time.sleep(300)


@AppMain.subcommand('reload')
class AppReload(cli.Application):

    def main(self):
        return uwsgi['--reload', '/tmp/uwsgi.pid'] & RETCODE(FG=True)


@AppMain.subcommand('migrate_db')
class AppDBMigrate(cli.Application):

    def main(self):
        local.env['FLASK_APP'] = 'run.py'
        return flask['db', 'migrate'] & RETCODE(FG=True)


@AppMain.subcommand('upgrade_db')
class AppDBUpgrade(cli.Application):

    def main(self):
        local.env['FLASK_APP'] = 'run.py'
        return flask['db', 'upgrade'] & RETCODE(FG=True)


@AppMain.subcommand('downgrade_db')
class AppDBDowngrade(cli.Application):

    def main(self):
        local.env['FLASK_APP'] = 'run.py'
        return flask['db', 'downgrade'] & RETCODE(FG=True)


@AppMain.subcommand('babel_update')
class BabelInit(cli.Application):

    def main(self):
        return pybabel['update', '-i', 'flexbi/messages.pot', '-d',
                       'flexbi/translations'] & RETCODE(FG=True)


@AppMain.subcommand('babel_compile')
class BabelCompile(cli.Application):

    def main(self):
        return pybabel['compile', '-f', '-d', 'flexbi/translations'] & RETCODE(
            FG=True)


if __name__ == '__main__':
    AppMain.run()
