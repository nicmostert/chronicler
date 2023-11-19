#!/usr/bin/env python

"""Tests for `annalist` package."""

import json

from annalist.annalist import Annalist
from tests.example_class import Craig, return_greeting


def test_singleton():
    """Test if Annalist is a singleton."""
    ann = Annalist()
    ann2 = Annalist()

    assert ann is ann2


def test_all_fields(capsys):
    """Test to see if all fields are captured."""
    format_str = (
        "{"
        + '"analyst_name": "%(analyst_name)s",\n'
        + '"function_name": "%(function_name)s",\n'
        + '"function_doc": "%(function_doc)s",\n'
        + '"ret_val": "%(ret_val)s",\n'
        + '"ret_val_type": "%(ret_val_type)s",\n'
        + '"ret_annotation": "%(ret_annotation)s",\n'
        + '"params": "%(params)s",\n'
        + '"asctime": "%(asctime)s",\n'
        + '"filename": "%(filename)s",\n'
        + '"funcName": "%(funcName)s",\n'
        + '"levelname": "%(levelname)s",\n'
        + '"levelno": "%(levelno)s",\n'
        + '"lineno": "%(lineno)s",\n'
        + '"message": "%(message)s",\n'
        + '"module": "%(module)s",\n'
        + '"msecs": "%(msecs)s",\n'
        + '"loggername": "%(name)s",\n'
        + '"pathname": "%(pathname)s",\n'
        + '"process": "%(process)s",\n'
        + '"processName": "%(processName)s",\n'
        + '"relativeCreated": "%(relativeCreated)s",\n'
        + '"stack_info": "%(stack_info)s",\n'
        + '"thread": "%(thread)s",\n'
        + '"threadName": "%(threadName)s",\n'
        + '"taskName": "%(taskName)s",\n'
        + '"additional_param": "%(additional_param)s"}'
    )

    ann = Annalist()
    ann.configure(
        analyst_name="test_all_fields",
        stream_format_str=format_str,
    )

    field_values = json.loads(
        '{"analyst_name": "test_all_fields",'
        '"function_name": "return_greeting",'
        '"function_doc": "Return a friendly greeting.",'
        '"ret_val": "Hi Craig",'
        '"ret_val_type": "<class \'str\'>",'
        '"ret_annotation": "<class \'str\'>",'
        "\"params\": \"{'name': {'default': 'loneliness', "
        "'annotation': <class 'str'>, 'kind': 'keyword', 'value': 'Craig'}}\","
        '"asctime": "unknown",'
        '"filename": "annalist.py",'
        '"funcName": "log_call",'
        '"levelname": "INFO",'
        '"levelno": "20",'
        '"lineno": "unknown",'
        '"message": "",'
        '"module": "annalist",'
        '"msecs": "unknown",'
        '"loggername": "auditor",'
        '"pathname": "/home/nic/repos/annalist/annalist/annalist.py",'
        '"process": "unknown",'
        '"processName": "MainProcess",'
        '"relativeCreated": "unknown",'
        '"stack_info": "None",'
        '"thread": "unknown",'
        '"threadName": "MainThread",'
        '"taskName": "None",'
        '"additional_param": "None"}'
    )

    return_greeting("Craig")

    captured = capsys.readouterr()
    # print(captured.err.split("{", maxsplit=1)[1])

    json_str = "{" + captured.err.split("{", maxsplit=1)[1]
    captured_fields = json.loads(json_str)

    for key, val in captured_fields.items():
        if field_values[key] != "unknown":
            assert val == field_values[key], f"Failing on {key}"


def test_init_logging(capsys):
    """Test logging of a constructor."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(name)s"

    ann.configure(
        analyst_name="test_init_logging",
        stream_format_str=format_str,
    )

    _ = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )

    captured = capsys.readouterr()

    assert captured.err == "test_init_logging | __init__ | auditor\n"


def test_setter_logging(capsys):
    """Test logging of a property setter."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(name)s"

    ann.configure(
        analyst_name="test_setter_logging",
        stream_format_str=format_str,
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )

    # Invoking the property setter here.
    cb.surname = "Coulomb"

    captured = capsys.readouterr()
    correct_out = "test_setter_logging | surname | auditor"
    assert captured.err.split("\n")[1] == correct_out


def test_message_logging(capsys):
    """Test logging of special message field."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(message)s"

    ann.configure(
        analyst_name="test_message_logging",
        stream_format_str=format_str,
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )

    cb.is_hurt_and_bearded()

    captured = capsys.readouterr()
    test_output = captured.err.split("\n")
    correct_out = (
        "test_message_logging | is_hurt_and_bearded | Adding a message easily"
    )
    assert test_output[1] == correct_out


def test_extra_info_logging(capsys):
    """Test logging of extra info fields."""
    ann = Annalist()

    format_str = (
        "%(analyst_name)s | %(function_name)s | %(injured)s | %(bearded)s"
    )

    ann.configure(
        analyst_name="test_extra_info_logging",
        stream_format_str=format_str,
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )

    cb.grow_craig(2)

    captured = capsys.readouterr()
    test_output = captured.err.split("\n")
    correct_out = "test_extra_info_logging | grow_craig | True | True"
    assert test_output[1] == correct_out


def test_logging_levels(capsys):
    """Test logging level propagation."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(levelname)s"

    ann.configure(
        analyst_name="test_logging_levels",
        stream_format_str=format_str,
        level_filter="WARNING",
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )

    # Should be suppressed
    cb.grow_craig(2)

    # Should log
    cb.shoesize = 11

    captured = capsys.readouterr()
    test_output = captured.err.split("\n")
    print(test_output)
    correct_out = "test_logging_levels | shoesize | ERROR"
    assert test_output[0] == correct_out
