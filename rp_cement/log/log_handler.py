import sys, os
import logging
from cement.ext.ext_colorlog import ColorLogHandler
from pythonjsonlogger import jsonlogger


class JsonFormatter(jsonlogger.JsonFormatter):

    # Internal, the name of the agent
    context_parameters = None

    def __init__(self, context_parameters=[]):
        super().__init__()
        self.context_parameters = context_parameters

    def add_fields(self, log_record, record, message_dict):
        super(JsonFormatter, self).add_fields(log_record, record, message_dict)
        extra_parameters = ["RUN_ID", "RD_JOB_NAME", "RD_JOB_ID", "RD_JOB_PROJECT"]
        for env_param in extra_parameters:
            if env_param in os.environ:
                log_record[env_param] = os.environ[env_param]
        log_record["levelname"] = record.levelname
        log_record["application_name"] = record.levelname


class LogHandler(ColorLogHandler):
    def a(self):
        return 5

    class Meta:
        label = "log_handler"

        # #: The logging format for the file logger.
        # file_format = "%(asctime)s (%(levelname)s) %(namespace)s : " + \
        #               "%(message)s"

        # #: The logging format for the consoler logger.
        if "APP_LOG_LOG_HANDLER_CONSOLE_FORMAT" in os.environ:
            console_format = os.environ["APP_LOG_LOG_HANDLER_CONSOLE_FORMAT"]
        else:
            console_format = "%(levelname)s: %(message)s"

        if "APP_LOG_LOG_HANDLER_FILE_FORMAT" in os.environ:
            file_format = os.environ["APP_LOG_LOG_HANDLER_FILE_FORMAT"]
        else:
            file_format = (
                "DEFAULT FILE FORMAT, Unused a everything is formatted by the JSON"
            )

    def _get_file_formatter(self, format):
        formatter = JsonFormatter()
        return formatter

    def _get_console_format(self):
        format = self._meta.console_format
        colorize = self.app.config.get("log.colorlog", "colorize_console_log")
        if sys.stdout.isatty() or "CEMENT_TEST" in os.environ:
            if colorize == True:
                format = "%(log_color)s" + format
        return format

    def _get_file_format(self):
        format = self._meta.file_format
        return format
