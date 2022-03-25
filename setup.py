# -*- coding: utf-8 -*-

from setuptools import find_namespace_packages, setup

NAMESPACE = "cro"

setup(
    name="cro.schedule",
    version="0.13.0",
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src", include=[f"{NAMESPACE}.*"]),
    install_requires=[
        "pandas",
        "requests",
        "openpyxl",
        "tqdm"
    ],
    extras_require={
        "test": ["pytest", "pytest-html"],
        "docs": ["sphinx", "jupyterlab"],
        "lint": ["black[jupyter]", "flake8", "isort", "mypy"],
    },
)
