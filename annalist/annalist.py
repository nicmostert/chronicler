"""Main module."""

import functools
import inspect
import logging


class FunctionLogger:
    def __init__(self, logger_name, analyst_name):
        self.logger = logging.getLogger(logger_name)
        self.analyst_name = analyst_name
        self.handler = logging.StreamHandler()  # Log to console
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
        )
        self.handler.setFormatter(formatter)
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)
        self.logger.log(logging.INFO, "Logger Initialized")

    def log_call(self, level, func, ret_val, *args, **kwargs):
        signature = inspect.signature(func)
        function_name = func.__name__
        function_doc = func.__doc__
        if signature.return_annotation == inspect._empty:
            ret_annotation = None
        else:
            ret_annotation = signature.return_annotation
        params = []
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

            param_attrs = {
                "name": name,
                "default": default_val,
                "annotation": annotation,
                "kind": kind,
                "value": value,
            }
            params += [param_attrs]

        self.logger.log(
            level,
            "\n============ Called function %s ============"
            "\nAnalyst: %s"
            "\nFunction name: %s"
            "\nFunction docstring: %s"
            "\nParameters: %s"
            "\nReturn Annotation: %s"
            "\nReturn Type: %s"
            "\nReturn Value: %s"
            "\n========================================"
            % (
                str(function_name),
                str(self.analyst_name),
                str(function_name),
                str(function_doc),
                str(params),
                str(ret_annotation),
                str(type(ret_val)),
                str(ret_val),
            ),
        )

    def annalize(self, _func=None, *, operation_type="PROCESS"):
        def decorator_logger(func):
            # This line reminds func that it is func and not the decorator
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                self.log_call(logging.INFO, func, result, *args, **kwargs)
                return result

            return wrapper

        # This section handles optional arguments passed to the logger
        if _func is None:
            return decorator_logger
        else:
            return decorator_logger(_func)


if __name__ == "__main__":
    # Initialize the custom logger
    logger = FunctionLogger("audit", "Nic Baby")

    @logger.annalize(operation_type="PROCESS")
    def example_function(a, b=1):
        """This is an example function."""
        result = a + b
        return result

    # Call the example function
    result = example_function(10, b=20)
    print(result)
