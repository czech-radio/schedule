# -*- coding: utf-8 -*-

from setuptools import setup, find_namespace_packages

NAMESPACE = "cro"

setup(
    name="cro.schedule",
    version="0.8.0",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", include=[f"{NAMESPACE}.*"]),
    install_requires=[
        "pandas",
        "requests",
    ],
    extras_require={
        "test": ["pytest", "pytest-html"],
        "docs": ["sphinx", "jupyterlab"],
        "lint": ["black", "flake8"],
    },
)
