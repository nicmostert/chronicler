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
        analyst_name="Test Two",
        file_format_str=format_str,
        stream_format_str=format_str,
        logfile="tests/logfile.txt",
    )

    field_values = json.loads(
        '{"analyst_name": "Test Two",'
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

    json_str = "{" + captured.err.split("{", maxsplit=1)[1]
    captured_fields = json.loads(json_str)

    for key, val in captured_fields.items():
        if field_values[key] != "unknown":
            assert val == field_values[key], f"Failing on {key}"


def test_init_logging(capsys):
    """Test logging of a constructor"""
    ann = Annalist()
    ann.configure()

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )

    assert cb.surname == "Beaven"


def test_extra_info_logging(caplog):
    """Test logger behaviour."""
    ann = Annalist()
    ann.configure(
        analyst_name="Testificate",
        # level_filter="WARNING",
        # default_level="DEBUG"
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )
    cb.grow_craig(2)
    cb.surname = "Coulomb"
    cb.shoesize = 11

    print(cb)
