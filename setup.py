import os
import re

from setuptools import find_packages, setup


def get_version(package):
    """
    Return package version as listed in `__version__` in `__init__.py`.
    """
    with open(os.path.join(package, "__init__.py")) as f:
        return re.search("__version__ = ['\"]([^'\"]+)['\"]", f.read()).group(1)


def get_long_description():
    """Return the README"""
    with open("README.md", encoding="utf8") as f:
        return f.read()


setup(
    name="aiosmartpost",
    python_requires=">=3.8",
    version=get_version("smartpost"),
    description="Itella SmartPost API wrapper for humans 📦",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/HarrySky/aiosmartpost",
    license="Unlicense",
    author="Igor Nehoroshev",
    author_email="mail@neigor.me",
    packages=find_packages(),
    # Use MANIFEST.in for data files
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # For HTTP requests to API using HTTP/2
        "httpx",
        "h2",
        # For parsing API responses to dict
        # (SmartPost API uses XML instead of JSON for some reason)
        "xmltodict",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: The Unlicense (Unlicense)",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Typing :: Typed",
    ],
)
