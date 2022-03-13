# -*- coding: utf-8 -*-

from setuptools import setup, find_namespace_packages

NAMESPACE = "cro"

setup(
    name="cro.schedule",
    version="0.2.0",
    install_requires=[
        "requests",
    ],
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", include=[f"{NAMESPACE}.*"]),
)