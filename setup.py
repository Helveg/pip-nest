#!/usr/bin/env python3
import os, sys
import setuptools

# Get text from README.txt
with open("README.md", "r") as fp:
    readme_text = fp.read()

# Get __version__ without importing
with open("pipnest/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__ = "):
            exec(line)
            break

setuptools.setup(
    name="pipnest",
    version=__version__,
    description="Distribute your extension module as a pip installable package",
    license="MIT",
    keywords="nest-simulator packaging module extension nest pip",
    author="Robin De Schepper",
    author_email="robingilbert.deschepper@unipv.it",
    url="https://github.com/Helveg/pipnest",
    long_description=readme_text,
    long_description_content_type="text/markdown",
    packages=["pipnest"],
    include_package_data=True,
    package_data={"pipnest": []},
    entry_points={"console_scripts": ["pipnest = pipnest.cli:handle_command"],
        "pipnest.actions": ["init = pipnest.cli:InitAction"]},
    classifiers=[
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=["setuptools"],
    extras_require={"dev": ["sphinx", "sphinx_rtd_theme>=0.4.3", "pre-commit", "black"],},
)
