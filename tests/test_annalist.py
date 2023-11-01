#!/usr/bin/env python

"""Tests for `annalist` package."""

from annalist.annalist import Annalist

ann = Annalist()
ann.configure("Test Logger", "Testificate")

correct_output = """
============ Called function len_of_string_example ============
Analyst: Testificate
Function name: len_of_string_example
Function docstring: None
Parameters: [{'name': 'str_arg', 'default': None, 'annotation': \
None, 'kind': 'keyword', 'value': 'This is a string'}]
Return Annotation: None
Return Type: <class 'int'>
Return Value: 16
========================================"""


@ann.annalize
def len_of_string_example(str_arg):
    """Calculate length of string."""
    return len(str_arg)


def test_decorator_logger_functionality(caplog):
    """Test logger behaviour."""
    str_example = "This is a string"
    result = len_of_string_example(str_example)
    print([dir(rec) for rec in caplog.records])
    print(caplog.records)
    log_messages = [rec.message for rec in caplog.records]
    print(log_messages)
    assert log_messages[0] == correct_output
    assert result == len(str_example)


def test_decorator_logger_wrapper():
    """Test decorator function directly."""

    def mock_func():
        print("Console Output to Intercept?")
        return "Mock function called."

    decorated_mock_func = ann.annalize(mock_func)

    result = decorated_mock_func()
    assert result == "Mock function called."
