==========
Annalist
==========

.. image:: https://img.shields.io/pypi/v/data-annalist.svg
        :target: https://pypi.python.org/pypi/data-annalist

.. image:: https://readthedocs.org/projects/annalist/badge/?version=latest
        :target: https://annalist.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://results.pre-commit.ci/badge/github/nicmostert/annalist/main.svg
   :target: https://results.pre-commit.ci/latest/github/nicmostert/annalist/main
   :alt: pre-commit.ci status

Audit trail generator for data processing scripts.


* Free software: GNU General Public License v3
* Documentation: https://annalist.readthedocs.io.

==================
Usage
==================

Create an ``Annalist`` object at the base of the module you'd like to audit. use the ``@Annalist.annalize`` decorator on any function you would like to annalize

::

    from annalist.annalist import Annalist
    from annalist.decorators import function_logger

    ann = Annalist()
    ann.configure()

    @function_logger
    def example_function():
        ...

Annalist also works on class methods, with the help of the ``ClassLogger`` decorator.

::

    from annalist.decorators import ClassLogger

    class ExampleClass():

        # Initializers can be annalized just fine
        @ClassLogger  # type: ignore
        __init__(self, arg1, arg2):
            self.arg1 = arg1
            self._arg2 = arg2
            ...

        # DO NOT put an annalizer on a property definition.
        # The annalizer calls the property itself, creating infinite recursion.
        @property
        def arg2(self):
            return self._arg2

        # Putting an annalizer on a setter is fine though.
        # Just make sure you put it after the setter decorator.
        @ClassLogger  # type: ignore
        @arg2.setter
        def arg2(self, value):
            self._arg2 = value

        # DO NOT put it on the __repr__ either.
        # Same as before, this creates infinite recursion.
        def __repr__(self):
            return f"{str(arg1)}: {str(arg2)}"

In the main script, the Annalist object must be called again. This will point to the singleton object initialized in the dependency. The annalist must be configured before usage.

    .. note:: MyPy issues

    Note the `# type: ignore` inline comments. These are only necessary when using `mypy`, which doesn't really seem to like decorators. They need to be supplied when decorating an `__init__` constructor method, or when adding multiple decorators to a method.

>>> ann = Annalist()
>>> ann.configure(logger_name="Example Logger", analyst_name="Speve")

Now the annalized code can be run like normal, and will be audited.

>>> example_function()
2023/11/2 09:42:13 | INFO | example_function called by Speve as part of Example Logger session


Formatters
-------------------

Annalist is built on the standard python *logging* library. Formatters can be specified in the same syntax as is documented in the `logging docs`. The available fields can be found in `Fields`.

Annalist supports two formatters. The *File formatters* formats the output to the logfile, and *Stream formatter* formats the console output.

::

    from annalist.annalist import Annalist

    ann = Annalist()
    ann.configure(...)

    ann.set_file_formatter(
        "%(asctime)s, %(analyst_name)s, example_funtion "
        "| %(message)s",
    )

    ann.set_stream_formatter(
        "%(asctime)s, %(function_name)s "
    )


In this example, the console output might be

>>> example_function()
2023/11/2 09:42:13, example_function

whereas the contents of the logfile might be:

::

    2023/11/2 09:42:13, example_function, Speve | This is an example.

Fields
___________

Annalist collects information about a decorated function and makes those available as fields. Additionally, the fields from the logging library are also available, although they are generally less useful. Below are all the useful features that are available. See all the logging fields `here`_.The reason for their limited usefulness are that most of the code references made there point to the annalist library, and not the decorated code.

All the fields that we consider useful are listed below:

.. _here: https://docs.python.org/3/library/logging.html#logrecord-attributes

+--------------------+----------------------------------------+---------------------+
| Field              | Description                            | Source              |
+====================+========================================+=====================+
| ``analyst_name``   | Name of the analyst writing the script | User configured     |
+--------------------+----------------------------------------+---------------------+
| ``function_name``  | Function Name                          | Function Inspection |
+--------------------+----------------------------------------+---------------------+
| ``function_doc``   | Function Docstring                     | Function Inspection |
+--------------------+----------------------------------------+---------------------+
| ``ret_val``        | Return value                           | Function Inspection |
+--------------------+----------------------------------------+---------------------+
| ``ret_val_type``   | Return value type                      | Function Inspection |
+--------------------+----------------------------------------+---------------------+
| ``ret_annotation`` | Annotation of return value             | Function Inspection |
+--------------------+----------------------------------------+---------------------+
| ``params``         | Input parameters                       | Function Inspection |
+--------------------+----------------------------------------+---------------------+
| ``asctime``        | Time of function call                  | Logging Library     |
+--------------------+----------------------------------------+---------------------+
| ``levelname``      | Logging level name                     | Logging Library     |
+--------------------+----------------------------------------+---------------------+
| ``levelno``        | Logging level number                   | Logging Library     |
+--------------------+----------------------------------------+---------------------+
| ``message``\*      | Needs to be passed as extra param      | Logging Library     |
+--------------------+----------------------------------------+---------------------+
| ``name``           | Logger name                            | Logging Library     |
+--------------------+----------------------------------------+---------------------+

The ``message`` field is an optional parameter that can be passed directly to the decorator. This is the simplest way to add more information to a function log.

::

    @function_logger(message="this is a message")
    def example_function():
        ...


You can also specify the level of the logger in the same way, as a decorator keword argument.

::

    @function_logger(level="DEBUG")
    def example_function():
        ...

Unfortunately, Annalist does not yet offer support of passing these fields into the ``@ClassLogger``. However, we can still get information to the logger by inspecting the method arguments, and the attributes on the class instance. Consider the following setup::

    from annalist.decorators import ClassLogger

    class MyClass:
        @ClassLogger  # type: ignore
        def __init__(attr, prop):
            self.attr = attr
            self._prop = prop

        @property
        def prop(self):
            return prop

        @ClassLogger  # type: ignore
        @prop.setter
        def prop(self, value):
            self._prop = value

        @ClassLogger
        def square_attr(self):
            return self.attr ** 2

        @ClassLogger
        def add_prop_to_attr(self):
            return attr + prop

        @ClassLogger  # type: ignore
        @staticmethod
        def increment_value(attr):
            return attr += 1

Note the two class attributes named ``attr`` and ``prop``. We can track these properties based on their variable names by passing it into the formatter:

>>> from annalist.annalist import Annalist
>>> ann = Annalist()
>>> ann.configure(...)
>>> ann.add_stream_formatter("%(function_name)s | prop: %(prop)s | attr: %(attr)s")

The ``ClassLogger`` decorator activates upon runtime and inspects the namespace. First, it looks for the attribute in the names of the input arguments of the decorated function. If found, it sends it to the formatter (See "Custom Fields"):

>>> mc = MyClass(7, 2)
>>> mc.prop = 3
prop | prop: 3 | attr: 7

Notice that the ``setter`` of ``prop`` caused ``ClassLogger`` to look for the values of ``prop`` and ``attr`` on the ``mc`` instance.

>>> mc.square_attr()
49
square_attr | prop: 3 | attr: 7

Notice how the function ``square_attr`` did not alter the value of ``attr``.

Because this logger is sensitive to the state of the logger, it is important to be weary of variable names.

>>> mc.increment_value(5)
6
square_attr | prop: 3 | attr: 5

Notice how, despite having no real reference to the attribute ``attr`` on the namespace, the logger found the input argument named ``attr``, and associated this with the attribute it is logging. I believe this to be a useful feature, but care should be taken when using it like this.

Custom Fields
--------------

Annalist accepts any number of arbitrary fields in the formatter. If these fields are not one of the fields available by default, the fields is dynamically added and processed. However, this field must then be passed to the decorator in the ``extra_info`` argument.

For example, you might set the formatter as follows. In this example, the fields ``site`` and ``hts_file`` are custom, and are not available by default.


::

    from annalist.annalist import Annalist

    ann = Annalist()
    ann.configure(...)

    ann.set_file_formatter(
        "%(asctime)s, %(analyst_name)s, %(site)s, %(hts_file)s "
        "| %(message)s",
    )

Then, passing those parameters into the example function looks like this:

::

    from annalist.decorators import function_logger
    hts_file = "file.hts"

    @function_logger(
        level="INFO",
        message="This decorator passes extra parameters",
        extra_info={
            "site_name": "Site one",
            "hts_file": hts_file,
        }
    )
    def example_function(arg1, arg2):
        ...


If the custom fields are not included in a function decorator, they will simply default to ``None``.

The ``function_logger`` can also be used in "wrapper" mode. This is useful when an undecorated function needs to be annalized at call-time::

    function_logger(
        example_function,
        level="INFO",
        message="This decorator passes extra parameters",
        extra_info={
            "site_name": "Site one",
            "hts_file": hts_file,
        }
    )(arg1, arg2)

When using Annalist in a class method, you might want to log class attributes. Unfortunately, the following syntax will not work, since the decorator has no knowledge of the class instance (self).

::

    class ExampleClass:
        ...

        @function_logger(
            level="INFO",
            message="This decorator passes extra parameters",
            extra_info={
                "site_name": self.site_name, # THIS DOES NOT WORK!
                "hts_file": self.hts_file, # THIS DOES NOT WORK!
            }
        )
        def example_method(self):
            ...


The way to track class attributes is to use the ``ClassLogger`` decorator. This decorator activates at runtime. Any custom fields passed to the Annalist formatter are noted, and ``ClassLogger`` inspects the class instance for attributes with the same name.

::

    from annalist.decorators import ClassLogger

    class ExampleClass:
        def __init__(self, attr):
            self.attr = attr

        @ClassLogger
        def example_function(self):
            ...

See annalist.decorators.ClassLogger for more details.

Levels
--------

Annalist uses the levels as defined in the logging library. Upon configuration, the ``default level`` can be set, which is the level at which all logs are logged unless overridden. The default value for ``default level`` is "INFO".

::

    ann.configure(
        analyst_name="Speve",
        stream_format_str=format_str,
        level_filter="WARNING",
    )

A annalized method can be logged at a raised or lowered level by specifying the logging level explicitely in the decorator:

::

    @function_logger(level="DEBUG")
    def untracked_function():
        ...

==================
Feature Roadmap
==================

This roadmap outlines the planned features and milestones for the development of our deterministic and reproducible process auditing system.

Milestone 1: Audit Logging Framework
------------------------------------

x Develop a custom audit logging framework or class.
x Capture function names, input parameters, return values, data types, and timestamps.
x Implement basic logging mechanisms for integration.

Milestone 1.5: Hilltop Auditing Parity
---------------------------------------
x Define custom fields and formatters
x Manage logger levels correctly

Milestone 2: Standardized Logging Format
-----------------------------------------
- Define a standardized logging format for comprehensive auditing.
- Ensure consistency and machine-readability of the logging format.

Milestone 3: Serialization and Deserialization
----------------------------------------------
- Implement serialization and deserialization mechanisms.
- Store and retrieve complex data structures and objects.
- Test serialization for data integrity.

Milestone 4: Versioning and Dependency Tracking
-----------------------------------------------
- Capture and log codebase version (Git commit hash) and dependencies.
- Ensure accurate logging of version and dependency information.

Milestone 5: Integration Testing
--------------------------------
- Create integration tests using the audit logging framework.
- Log information during the execution of key processes.
- Begin development of process recreation capability.

Milestone 6: Reproduction Tool (Partial)
----------------------------------------
- Develop a tool or script to read and reproduce processes from the audit trail.
- Focus on recreating the environment and loading serialized data.

Milestone 7: Documentation (Partial)
--------------------------------------
- Create initial documentation.
- Explain how to use the audit logging framework and the audit trail format.
- Document basic project functionalities.

Milestone 8: Error Handling
---------------------------
- Implement robust error handling for auditing and reproduction code.
- Gracefully handle potential issues.
- Provide informative and actionable error messages.

Milestone 9: MVP Testing
-------------------------
- Conduct testing of the MVP.
- Reproduce processes from the audit trail and verify correctness.
- Gather feedback from initial users within the organization.

Milestone 10: MVP Deployment
------------------------------
- Deploy the MVP within the organization.
- Make it available to relevant team members.
- Encourage usage and collect user feedback.

Milestone 11: Feedback and Iteration
--------------------------------------
- Gather feedback from MVP users.
- Identify shortcomings, usability issues, or missing features.
- Prioritize and plan improvements based on user feedback.

Milestone 12: Scaling and Extending
------------------------------------
- Explore scaling the solution to cover more processes.
- Add additional features and capabilities to enhance usability.

Please note that milestones may overlap, and the order can be adjusted based on project-specific needs. We aim to remain flexible and responsive to feedback during development.

=======
Credits
=======

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
