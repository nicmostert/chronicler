"""Main module."""

import logging

GET_DATA = 25
PROCESS = 26
PUT_DATA = 27

logging.addLevelName(GET_DATA, "GET_DATA")
logging.addLevelName(PROCESS, "PROCESS")
logging.addLevelName(PUT_DATA, "PUT_DATA")


auditor = logging.getLogger("auditor")
handler = logging.StreamHandler()
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
handler.setFormatter(formatter)
auditor.addHandler(handler)
auditor.setLevel(GET_DATA)


def decorator_logger(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        function_name = func.__name__
        function_class = func.__class__
        function_module = func.__module__
        function_dir = dir(func)
        function_doc = func.__doc__
        auditor.log(PROCESS, function_name)
        auditor.log(PROCESS, function_class)
        auditor.log(PROCESS, function_module)
        auditor.log(PROCESS, function_dir)
        auditor.log(PROCESS, function_doc)
        return result

    return wrapper
