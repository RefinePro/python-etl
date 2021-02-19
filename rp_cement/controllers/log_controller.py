from cement import ex
from .base_controller import BaseController
import peewee as pw
import peeweedbevolve


class LogController(BaseController):
    class Meta:
        label = "rp-log"
        stacked_on = "base"
        stacked_type = "embedded"

    @ex(help="Test the logging system by printing message of all levels")
    def log_test(self):
        """Example sub-command."""
        self.app.log.debug("This is a debug message.")
        self.app.log.info("This is a debug message.")
        self.app.log.warning("This is a debug message.")
        self.app.log.error("This is a debug message.")
        self.app.log.fatal("This is a debug message.")

    @ex(help="Test the logging system by printing message of all levels")
    def log_config(self):
        """Example sub-command."""
        self.dump(self.app.config.get_dict())

    @ex(help="Test the method to dump an object")
    def log_test_dump(self):
        """Example sub-command."""
        complex_var = {"hey": "you", "i am": {"deeply": {"0": ["0", "nested"]}}}
        self.dump(complex_var)

    @ex(help="Test the method to dump a (complex) object, like an instance or a Class")
    def log_test_inspect(self):
        self.inspect(self.app)
