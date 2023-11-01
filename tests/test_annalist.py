#!/usr/bin/env python

"""Tests for `annalist` package."""

from annalist.annalist import Annalist
from tests.example_class import Craig

ann = Annalist()
ann.configure("Test Logger", "Testificate")

correct_output = """
============ Called function __init__ ============
Analyst: Testificate
Function name: __init__
Function docstring: Initialize a Craig.
Parameters: [{'name': 'self', 'default': None, 'annotation': None, 'kind': \
'keyword', 'value': Craig Beaven is 5.5 ft tall and wears size 9 shoes.}, \
{'name': 'surname', 'default': None, 'annotation': <class 'str'>, 'kind': \
'keyword', 'value': 'Beaven'}, {'name': 'height', 'default': None, \
'annotation': <class 'float'>, 'kind': 'keyword', 'value': 5.5}, \
{'name': 'shoesize', 'default': None, 'annotation': <class 'int'>, \
'kind': 'keyword', 'value': 9}]
Return Annotation: None
Return Type: <class 'NoneType'>
Return Value: None
========================================"""


def test_init_logging(caplog):
    """Test logger behaviour."""
    cb = Craig("Beaven", 5.5, 9)
    print(cb)
    print([dir(rec) for rec in caplog.records])
    print(caplog.records)
    log_messages = [rec.message for rec in caplog.records]
    print(log_messages)
    assert log_messages[0] == correct_output


def test_annalizer_wrapper():
    """Test decorator function directly."""

    def mock_func():
        print("Console Output to Intercept?")
        return "Mock function called."

    decorated_mock_func = ann.annalize(mock_func)

    result = decorated_mock_func()
    assert result == "Mock function called."
