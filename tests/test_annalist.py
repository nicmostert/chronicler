#!/usr/bin/env python

"""Tests for `annalist` package."""

import inspect
import json

from annalist.annalist import Annalist
from annalist.decorators import function_logger
from tests.example_class import Craig, return_greeting, which_craig_is_that


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
        + '"injured": "%(injured)s"}'
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
        '"message": "Just saying hi.",'
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
        '"injured": "Yessir."}'  # Extra parameter, user specified.
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


def test_nested_method_logging(capsys):
    """Test logging of a decorated method that calls another."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | height: %(height)s"

    ann.configure(
        analyst_name="test_nested_method_logging",
        stream_format_str=format_str,
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )

    assert cb.height == 5.5

    # This one changes height, which is annalized also.
    cb.grow_craig(1.5)

    assert cb.height == 7.0

    captured = capsys.readouterr()
    correct_out = [
        "test_nested_method_logging | __init__ | height: 5.5",
        "test_nested_method_logging | height | height: 7.0",
        "test_nested_method_logging | grow_craig | height: 7.0",
    ]

    test_output = captured.err.split("\n")

    assert test_output[0] == correct_out[0]
    assert test_output[1] == correct_out[1]
    assert test_output[2] == correct_out[2]


def test_static_method_logging(capsys):
    """Test logging of a static."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(ret_val)s"

    ann.configure(
        analyst_name="test_static_method_logging",
        stream_format_str=format_str,
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=False,
    )

    # This one changes height, which is annalized also.
    cb.what_is_a_craig()

    captured = capsys.readouterr()
    correct_out = [
        "test_static_method_logging | __init__ | None",
        "test_static_method_logging | what_is_a_craig | They sit next to me.",
    ]

    test_output = captured.err.split("\n")

    assert test_output[0] == correct_out[0]
    assert test_output[1] == correct_out[1]


def test_normal_method_logging(capsys):
    """Test logging of a normal method."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(ret_val)s"

    ann.configure(
        analyst_name="test_normal_method_logging",
        stream_format_str=format_str,
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=False,
    )

    # This one changes height, which is annalized also.
    cb.is_hurt_and_bearded()

    captured = capsys.readouterr()
    correct_out = [
        "test_normal_method_logging | __init__ | None",
        "test_normal_method_logging | is_hurt_and_bearded | False",
    ]

    test_output = captured.err.split("\n")

    assert test_output[0] == correct_out[0]
    assert test_output[1] == correct_out[1]


def test_class_method_logging(capsys):
    """Test logging of a classmethod."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(levelname)s"

    ann.configure(
        analyst_name="test_class_method_logging",
        stream_format_str=format_str,
    )

    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=False,
    )

    craig_surnames = ["Fisher", "Stewart-Baxter"]

    # This one changes height, which is annalized also.
    cb.army_of_craigs(craig_surnames)

    captured = capsys.readouterr()
    correct_out = [
        "test_class_method_logging | __init__ | INFO",
        "test_class_method_logging | __init__ | INFO",
        "test_class_method_logging | __init__ | INFO",
        "test_class_method_logging | army_of_craigs | INFO",
    ]

    test_output = captured.err.split("\n")

    assert test_output[0] == correct_out[0]
    assert test_output[1] == correct_out[1]
    assert test_output[2] == correct_out[2]
    assert test_output[3] == correct_out[3]


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

    cb.surname = "Pilkington"

    cb.is_hurt_and_bearded()

    captured = capsys.readouterr()
    test_output = captured.err.split("\n")
    correct_out = [
        "test_message_logging | __init__ | METHOD Craig.__init__ "
        + "takes args () and kwargs {'surname': 'Beaven', "
        + "'height': 5.5, 'shoesize': 9, 'injured': True, "
        + "'bearded': True}. It is on an instance of "
        + "Craig, and returns the value None.",
        "test_message_logging | surname | PROPERTY Craig.surname "
        + "SET TO Pilkington. It is on an instance of Craig.",
        "test_message_logging | is_hurt_and_bearded | METHOD "
        + "Craig.is_hurt_and_bearded takes args () and kwargs {}. "
        + "It is on an instance of Craig, and returns the value True.",
    ]

    assert test_output[0] == correct_out[0]
    assert test_output[1] == correct_out[1]
    assert test_output[2] == correct_out[2]


def test_class_attribute_logging(capsys):
    """Test logging of extra info fields."""
    ann = Annalist()

    format_str = (
        "%(analyst_name)s | %(function_name)s | %(height)s "
        "| %(injured)s | %(bearded)s"
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
        bearded=False,
    )

    cb.grow_craig(2)

    captured = capsys.readouterr()
    test_output = captured.err.split("\n")
    correct_out = [
        "test_extra_info_logging | __init__ | 5.5 | True | False",
        "test_extra_info_logging | height | 7.5 | True | False",
        "test_extra_info_logging | grow_craig | 7.5 | True | False",
    ]
    assert test_output[0] == correct_out[0]
    assert test_output[1] == correct_out[1]
    assert test_output[2] == correct_out[2]


def test_logging_levels(capsys):
    """Test logging level propagation."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(levelname)s"

    ann.configure(
        analyst_name="test_logging_levels",
        stream_format_str=format_str,
        level_filter="WARNING",
    )

    # should be suppressed.
    ann.logger.info("Message doesn't matter")

    # Should log
    ann.logger.error("No message field in the formatter")

    # Should log
    function_logger(which_craig_is_that, level="WARNING")("right")

    # Should be suppressed
    cb = Craig(
        surname="Beaven",
        height=5.5,
        shoesize=9,
        injured=True,
        bearded=True,
    )

    ann.default_level = "WARNING"

    # Should log
    cb.shoesize = 11

    correct_out = [
        "None | None | ERROR",
        "test_logging_levels | which_craig_is_that | WARNING",
        "test_logging_levels | shoesize | WARNING",
    ]
    captured = capsys.readouterr()
    test_output = captured.err.split("\n")

    assert test_output[0] == correct_out[0]
    assert test_output[1] == correct_out[1]
    assert test_output[2] == correct_out[2]


def test_redecoration(capsys):
    """Test logging level propagation."""
    ann = Annalist()

    format_str = "%(analyst_name)s | %(function_name)s | %(message)s"

    ann.configure(
        analyst_name="test_redecoration",
        stream_format_str=format_str,
    )

    # Undecorated - no logging
    which_craig_is_that("Left")

    function_logger(
        which_craig_is_that,
        message="Inline decoration of an undecorated function.",
    )("right")

    # Already decorated
    return_greeting("Craig")

    # Redecorating a decorated function

    function_logger(
        inspect.unwrap(return_greeting), message="Redecorated message"
    )("Speve")

    correct_out = [
        "test_redecoration | which_craig_is_that | "
        "Inline decoration of an undecorated function.",
        "test_redecoration | return_greeting | Just saying hi.",
        "test_redecoration | return_greeting | Redecorated message",
    ]
    captured = capsys.readouterr()
    test_output = captured.err.split("\n")

    assert test_output[0] == correct_out[0]
    assert test_output[1] == correct_out[1]
    assert test_output[2] == correct_out[2]
