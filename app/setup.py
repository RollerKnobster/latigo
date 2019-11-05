#!/usr/bin/env python

import os
from setuptools import setup, find_packages


setup_requirements = ["pytest-runner", "setuptools_scm"]


def read(fname):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    print(f"Reading from {fn}")
    if os.path.exists(fn):
        with open(fn) as f:
            return f.read()
    return ""


def read_requirements(fname: str):
    fn = os.path.join(os.path.dirname(os.path.abspath(__file__)), fname)
    print(f"Reading requirements from {fn}")
    with open(fn) as f:
        return [r.strip() for r in f.readlines()]
    return []


setup(
    name="latigo",
    version="0.0.2",
    author="Lennart Rolland",
    author_email="lroll@equinor.com",
    description=("A continuous prediction service that uses Gordo to predict data for IOC"),
    license="AGPL-3.0",
    keywords="gordo ioc continuous prediction",
    url="https://github.com/equinor/latigo",
    packages=find_packages(),
    setup_requires=setup_requirements,
    zip_safe=True,
    long_description=read("README.md"),
    install_requires=read_requirements("requirements.in"),  # Allow flexible deps for install
    tests_require=read_requirements("test_requirements.txt"), # Use rigid deps for testing
    test_suite="../tests",
    python_requires="~=3.7.4",
    include_package_data=True,
    # From https://pypi.org/pypi?%3Aaction=list_classifiers
    classifiers=["Development Status :: 3 - Alpha", "Intended Audience :: Developers", "Intended Audience :: Other Audience", "Topic :: Utilities", "License :: OSI Approved :: GNU Affero General Public License v3", "Natural Language :: English", "Operating System :: POSIX :: Linux", "Programming Language :: Python :: 3.7", "Topic :: Other/Nonlisted Topic"],
)
