# !/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pycamunda',
    version='0.0.1b1',
    author='Peter Klauke',
    description='A high-level framework for communicating with the workflow and decision automation engine Camunda.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/pklauke/pycamunda',
    packages=['pycamunda'],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
    install_requires=['requests>=2.0.0']
)
