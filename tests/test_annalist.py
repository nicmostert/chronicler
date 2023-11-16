#!/usr/bin/env python

"""Tests for `annalist` package."""

from annalist.annalist import Annalist
from tests.example_class import Craig

correct_output = """
============ Called function __init__ ============
Analyst: Testificate
Function name: __init__
Function docstring: Initialize a Craig.
Parameters: [\
{'name': 'self', 'default': None, 'annotation': None, 'kind': \
'keyword', 'value': Craig Beaven is 5.5 ft tall and wears size 9 shoes.}, \
{'name': 'surname', 'default': None, 'annotation': <class 'str'>, 'kind': \
'keyword', 'value': 'Beaven'}, {'name': 'height', 'default': None, \
'annotation': <class 'float'>, 'kind': 'keyword', 'value': 5.5}, \
{'name': 'shoesize', 'default': None, 'annotation': <class 'int'>, \
'kind': 'keyword', 'value': 9}, {'name': 'injured', 'default': None, \
'annotation': <class 'bool'>, 'kind': 'keyword', 'value': True}, \
{'name': 'bearded', 'default': None, 'annotation': <class 'bool'>, \
'kind': 'keyword', 'value': True}]
Return Annotation: None
Return Type: <class 'NoneType'>
Return Value: None
========================================"""

#
# def test_init_logging(caplog):
#     """Test logger behaviour."""
#     ann = Annalist()
#     ann.configure("tests/logfile.txt", "Testificate")
#
#     # ann.set_file_formatter(
#     #     "%(asctime)s, %(analyst_name)s " +
#     #     "| %(injured)s, %(bearded)s " +
#     #     "| %(message)s",
#     # )
#
#     ann.set_stream_formatter(
#         "%(asctime)s, %(function_name)s, %(function_doc)s "
#         "| %(injured)s, %(bearded)s "
#         "| %(message)s",
#     )
#
#     cb = Craig("Beaven", 5.5, 9, True, True)
#     print(cb)
#     print([dir(rec) for rec in caplog.records])
#     print(caplog.records)
#     log_messages = [rec.message for rec in caplog.records]
#     print(log_messages)
#     assert log_messages[0] == correct_output
#


def test_extra_info_logging(caplog):
    """Test logger behaviour."""
    ann = Annalist()
    ann.configure("tests/logfile.txt", "Testificate")

    # ann.set_file_formatter(
    #     "%(asctime)s, %(analyst_name)s " +
    #     "| %(injured)s, %(bearded)s " +
    #     "| %(message)s",
    # )

    ann.set_stream_formatter(
        "%(asctime)s, %(function_name)s, %(function_doc)s "
        "| %(injured)s, %(bearded)s "
        "| %(params)s",
    )

    cb = Craig("Beaven", 5.5, 9, True, True)

    cb.grow_craig(2)
    cb.surname = "Coulomb"
    cb.shoesize = 11

    print(cb)


# def test_annalizer_wrapper():
#     """Test decorator function directly."""
#
#     ann = Annalist()
#     ann.configure("tests/logfile.txt", "Testificate")
#
#     def mock_func():
#         print("Console Output to Intercept?")
#         return "Mock function called."
#
#     decorated_mock_func = ann.annalize(mock_func)
#
#     result = decorated_mock_func()
#     assert result == "Mock function called."
