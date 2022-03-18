# -*- coding: utf-8 -*-

from setuptools import setup, find_namespace_packages

NAMESPACE = "cro"

setup(
    name="cro.schedule",
    version="0.4.0",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", include=[f"{NAMESPACE}.*"]),
    install_requires=[
        "requests",
    ],
    extras_require={
        "test": ["pytest", "pytest-html"],
        "docs": ["sphinx"],
        "lint": ["black", "flake8"],
    },
)
