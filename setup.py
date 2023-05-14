from pathlib import Path
from stay import load
from setuptools import setup, find_packages

with open("META.stay") as f:
    for meta in load(f):
        pass

LONG_DESCRIPTION = Path("README.md").read_text()

setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    zip_safe=False,
    **meta
)
