#!/usr/bin/env python

"""Tests for `annalist` package."""

from annalist.annalist import decorator_logger


@decorator_logger
def len_of_string_example(str_arg):
    return len(str_arg)


def test_decorator_logger_functionality(caplog):
    """Test logger behaviour"""
    str_example = "This is a string"
    result = len_of_string_example(str_example)
    print([dir(rec) for rec in caplog.records])
    log_messages = [rec.message for rec in caplog.records]
    assert log_messages == "whatsit"
    assert result == len(str_example)


def test_decorator_logger_wrapper():
    """Test decorator function directly"""

    def mock_func():
        print("Console Output to Intercept?")
        return "Mock function called."

    decorated_mock_func = decorator_logger(mock_func)

    result = decorated_mock_func()
    assert result == "Mock function called."
