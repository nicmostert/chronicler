#!/usr/bin/env python

"""The setup script."""

from setuptools import find_packages, setup

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

requirements: list[str] = []

test_requirements = [
    "pytest>=3",
]

setup(
    author="Nic Mostert",
    author_email="nicolas.mostert@horizons.govt.nz",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.10",
    ],
    description="Audit trail generator for data processing scripts.",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + "\n\n" + history,
    include_package_data=True,
    keywords="annalist",
    name="data-annalist",
    packages=find_packages(include=["annalist", "annalist.*"]),
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/nicmostert/annalist.git",
    version="0.3.2",
    zip_safe=False,
)
