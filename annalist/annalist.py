"""Main module."""

import functools
import inspect
import logging
import re
from os import PathLike

LOGGER_LEVELS = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
}


class FunctionLogger(logging.Logger):
    def __init__(self, name, extra_attributes):
        if extra_attributes:
            self.extra_attributes = extra_attributes
        else:
            self.extra_attributes = []
        logging.Logger.__init__(self, name)
        logging.Logger.setLevel(self, logging.INFO)
        self.propagate = True

    def add_attributes(self, extra_attributes: list):
        self.extra_attributes += extra_attributes

    def makeRecord(self, *args, **kwargs):
        rv = super().makeRecord(*args, **kwargs)
        for attr in self.extra_attributes:
            rv.__dict__[attr] = rv.__dict__.get(attr, None)
        return rv


class Singleton(type):
    """Singleton Metaclass.

    Ensures that only one instance of the inheriting class is created.
    """

    def __init__(self, name, bases, mmbs):
        """Enforce singleton upon new object creation."""
        super().__init__(name, bases, mmbs)
        self._instance = super().__call__()

    def __call__(self, *args, **kw):
        """Retrieve singleton object."""
        return self._instance


class Annalist(metaclass=Singleton):
    """Annalist Class."""

    _configured = False

    def __init__(self):
        """Not a true init I guess."""
        self.logger = FunctionLogger("TempLogger", None)
        self.stream_handler = logging.StreamHandler()  # Log to console

    def configure(
        self,
        logfile: str | PathLike[str] | None = None,
        analyst_name: str | None = None,
        file_format_str: str | None = None,
        stream_format_str: str | None = None,
        level_filter: str = "INFO",
        default_level: str = "INFO",
    ):
        """Configure the Annalist."""
        self._analyst_name = analyst_name

        extra_attributes = []

        if file_format_str:
            file_format_attrs = self.parse_formatter(file_format_str)
            extra_attributes += file_format_attrs

        if stream_format_str:
            stream_format_attrs = self.parse_formatter(stream_format_str)
            extra_attributes += stream_format_attrs

        default_formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(analyst_name)s"
        )
        # Set up formatters
        if file_format_str:
            self.file_formatter = logging.Formatter(file_format_str)
        else:
            self.file_formatter = default_formatter
        if stream_format_str:
            self.stream_formatter = logging.Formatter(stream_format_str)
        else:
            self.stream_formatter = default_formatter

        self.logfile = logfile

        # Set up handlers
        if self.logfile:
            self.file_handler = logging.FileHandler(self.logfile)
        self.stream_handler = logging.StreamHandler()  # Log to console

        default_attributes = [
            "analyst_name",
            "function_name",
            "function_doc",
            "ret_annotation",
            "params",
            "ret_val",
            "ret_val_type",
        ]

        all_attributes = default_attributes + extra_attributes

        self.default_level = LOGGER_LEVELS[default_level]

        self.logger = FunctionLogger("auditor", all_attributes)

        if self.logfile:
            self.logger.addHandler(self.file_handler)
        self.logger.addHandler(self.stream_handler)

        if self.logfile:
            self.file_handler.setFormatter(self.file_formatter)

        self.stream_handler.setFormatter(self.stream_formatter)
        # self.set_stream_formatter(self.stream_formatter)

        self.level_filter = LOGGER_LEVELS[level_filter]

        self.logger.setLevel(self.level_filter)

        # Adding some more fields to the logger this way
        self._configured = True

    @property
    def analyst_name(self):
        """The analyst_name property."""
        if not self._configured:
            raise ValueError(
                "Annalist not configured. Configure object after retrieval."
            )
        return self._analyst_name

    @analyst_name.setter
    def analyst_name(self, value):
        if not self._configured:
            raise ValueError(
                "Annalist not configured. Configure object after retrieval."
            )
        self._analyst_name = value

    @staticmethod
    def parse_formatter(format_string):
        return re.findall(r"%\((.*?)\)", format_string)

    def set_file_formatter(
        self, formatter, logfile: str | PathLike[str] | None = None
    ):
        """Change the file formatter of the logger."""
        if self.logfile is None:
            if logfile is None:
                raise ValueError(
                    "Cannot set up file formatter, no log file specified."
                )
            else:
                self.logfile = logfile
            self.file_handler = logging.FileHandler(self.logfile)
        else:
            self.logger.removeHandler(self.file_handler)
            self.file_handler = logging.FileHandler(self.logfile)

        file_format_attrs = self.parse_formatter(formatter)
        self.logger.add_attributes(file_format_attrs)
        self.file_formatter = logging.Formatter(formatter)
        self.file_handler.setFormatter(self.file_formatter)
        self.logger.addHandler(self.file_handler)

    def set_stream_formatter(self, formatter):
        """Change the stream formatter of the logger."""
        stream_format_attrs = self.parse_formatter(formatter)
        self.logger.add_attributes(stream_format_attrs)
        self.logger.removeHandler(self.stream_handler)
        self.stream_formatter = logging.Formatter(formatter)
        self.stream_handler = logging.StreamHandler()
        self.stream_handler.setFormatter(self.stream_formatter)
        self.logger.addHandler(self.stream_handler)

    def log_call(
        self, message, level, func, ret_val, extra_data, *args, **kwargs
    ):
        """Log function call."""
        if not self._configured:
            raise ValueError(
                "Annalist not configured. Configure object after retrieval."
            )

        report = {}
        signature = inspect.signature(func)
        report["function_name"] = func.__name__
        report["function_doc"] = func.__doc__
        if signature.return_annotation == inspect._empty:
            report["ret_annotation"] = None
        else:
            report["ret_annotation"] = signature.return_annotation

        params = {}
        all_args = list(args) + list(kwargs.values())
        for i, ((name, param), arg) in enumerate(
            zip(signature.parameters.items(), all_args)
        ):
            if param.default == inspect._empty:
                default_val = None
            else:
                default_val = param.default

            if param.annotation == inspect._empty:
                annotation = None
            else:
                annotation = param.annotation

            if i > len(args):
                kind = "positional"
                value = arg
            else:
                kind = "keyword"
                value = arg
            params[name] = {
                "default": default_val,
                "annotation": annotation,
                "kind": kind,
                "value": value,
            }
        report["params"] = params

        report["analyst_name"] = self.analyst_name
        report["ret_val_type"] = type(ret_val)
        report["ret_val"] = ret_val

        if extra_data:
            for key, val in extra_data.items():
                report[key] = val

        if level:
            logger_level = LOGGER_LEVELS[level]
        else:
            logger_level = self.default_level

        self.logger.log(
            logger_level,
            message,
            extra=report,
        )

    def annalize(
        self,
        _func=None,
        message: str = "",
        level: str | None = None,
        *,
        extra_info: dict | None = None,
    ):
        """I'm really not sure how this is going to work."""

        def decorator_logger(func):
            # This line reminds func that it is func and not the decorator
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.log_call(
                    message, level, func, result, extra_info, *args, **kwargs
                )
                return result

            return wrapper

        # This section handles optional arguments passed to the logger
        if _func is None:
            return decorator_logger
        else:
            return decorator_logger(_func)

    def annalize_class(
        self,
    ):
        pass
