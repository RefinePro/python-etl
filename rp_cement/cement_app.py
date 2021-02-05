from cement import CaughtSignal, App
from rp_cement.controllers.database_controller import *
from rp_cement.controllers.log_controller import *
from rp_cement.log.log_handler import LogHandler

from rich.console import Console
from rich import inspect
console = Console()

def configure_database(app):
    dsn = app.config.get('APP', 'database')

    if dsn:
        from playhouse.db_url import connect
        from models.db import db
        dsn = app.config.get('APP', 'database')
        app.log.debug('Initialized database')
        db.initialize(connect(dsn))
    else:
        app.log.debug('No database to initialize')




# def extend_app(app):
#     app.extend('inspect', inspect_var)

class CementApp(App):



    def inspect(self, var):
        inspect(var, methods=True)

    def dump(self, var):
        console.log(var, log_locals=False)

    class Meta:
        handlers = [DatabaseController, LogController, LogHandler]
        
        extensions = []
        
        log_handler = 'log_handler'

        config_section = 'APP'

        config_defaults = {
            'log.log_handler': {
                'level': 'DEBUG',
                'file': './var/log/log.log',
            },
            'log.colorlog': {
                'debug': True, # necessary but overrriden by log.log_handler
                'level': 'DEBUG', # necessary but overrriden by log.log_handler
                'to_console': True, 
                'rotate': True,
                'max_bytes': 512000,
                'max_files': 4,                
                'colorize_console_log': True,
                'colorize_file_log': False
            },
            'APP': {
                'database': None
            }
        }

        hooks = [
            ('pre_run', configure_database),
            # ('post_setup', extend_app),
        ]

        # # call sys.exit() on close
        close_on_exit = True