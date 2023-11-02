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

    ann = Annalist()

    @ann.annalize
    def example_function():
        ...

Annalise also works on most class functions, with some exceptions.

::

    class ExampleClass():

        # Initializers can be annalized just fine
        @ann.annalize
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
        @arg2.setter
        @ann.annalize
        def arg2(self, value):
            self._arg2 = value

        # DO NOT put it on the __repr__ either.
        # Same as before, this creates infinite recursion.
        def __repr__(self):
            return f"{str(arg1)}: {str(arg2)}"


In the main script, the Annalist object must be called again. This will point to the singleton object initialized in the dependency. The annalist must be configured before usage.

>>> ann = Annalist()
>>> ann.configure(logger_name="Example Logger", analyst_name="Speve")

Now the annalized code can be run like normal, and will be audited.

>>> example_function()
2023/11/2 09:42:13 | INFO | example_function called by Speve as part of Example Logger session



==================
Feature Roadmap
==================

This roadmap outlines the planned features and milestones for the development of our deterministic and reproducible process auditing system.

Milestone 1: Audit Logging Framework
------------------------------------

- Develop a custom audit logging framework or class.
- Capture function names, input parameters, return values, data types, and timestamps.
- Implement basic logging mechanisms for integration.

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
