from cement import CaughtSignal, App
from rp_cement.controllers.database_controller import *
from rp_cement.controllers.etl_controller import *
from rp_cement.controllers.log_controller import *
from rp_cement.log.log_handler import LogHandler
from cement import shell
from rich.console import Console
from rich import inspect

console = Console()
import os


def configure_database(app):
    dsn = app.config.get("APP", "database")

    if dsn:
        from playhouse.db_url import connect
        from models.db import db

        dsn = app.config.get("APP", "database")
        app.log.debug("Initialized database")
        db.initialize(connect(dsn))
    else:
        app.log.debug("No database to initialize")


# def extend_app(app):
#     app.extend('inspect', inspect_var)


class CementApp(App):
    def inspect(self, var):
        inspect(var, methods=True)

    def dump(self, var):
        console.log(var, log_locals=False)

    def debug(self, *args):
        message = " ".join([str(m) for m in args])
        self.log.debug(message)

    def info(self, *args):
        message = " ".join([str(m) for m in args])
        self.log.info(message)

    def warning(self, *args):
        message = " ".join([str(m) for m in args])
        self.log.warning(message)

    def error(self, *args):
        message = " ".join([str(m) for m in args])
        self.log.error(message)

    def fatal(self, *args):
        message = " ".join([str(m) for m in args])
        self.log.fatal(message)

    def simple_cmd(self, cmd, log=True):
        if log:
            self.log.info("Run command " + cmd)
        out, err, code = shell.cmd(cmd)
        if err:
            self.log.fatal(err)
            raise Exception(err)

        lines = out.splitlines()
        out_lines = []
        for line in lines:
            decoded = line.decode("utf-8").strip()
            if decoded:
                self.log.info(decoded)
                out_lines.append(decoded)
            else:
                out_lines.append(line)

        return out_lines

    class Meta:
        handlers = [DatabaseController, LogController, LogHandler, ETLController]

        extensions = []

        log_handler = "log_handler"

        config_section = "APP"

        config_defaults = {
            "log.log_handler": {
                "level": "DEBUG",
                "file": "./var/log/log.log",
            },
            "log.colorlog": {
                "debug": True,  # necessary but overrriden by log.log_handler
                "level": "DEBUG",  # necessary but overrriden by log.log_handler
                "to_console": True,
                "rotate": True,
                "max_bytes": 512000,
                "max_files": 4,
                "colorize_console_log": True,
                "colorize_file_log": False,
            },
            "APP": {"database": None, "data_dir": os.path.join(os.getcwd(), "var")},
        }

        hooks = [
            ("pre_run", configure_database),
            # ('post_setup', extend_app),
        ]

        # # call sys.exit() on close
        close_on_exit = True
