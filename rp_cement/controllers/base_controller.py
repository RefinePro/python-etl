from cement import Controller


class BaseController(Controller):
    def dump(self, var):
        self.app.dump(var)

    def inspect(self, var):
        self.app.inspect(var)

    def debug(self, *args):
        message = " ".join([str(m) for m in args])
        self.app.log.debug(message)

    def info(self, *args):
        message = " ".join([str(m) for m in args])
        self.app.log.info(message)

    def warning(self, *args):
        message = " ".join([str(m) for m in args])
        self.app.log.warning(message)

    def error(self, *args):
        message = " ".join([str(m) for m in args])
        self.app.log.error(message)

    def fatal(self, *args):
        message = " ".join([str(m) for m in args])
        self.app.log.fatal(message)
