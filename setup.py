
from stay import load
from setuptools import setup, find_packages

with open("META.stay") as f:
    for meta in load(f):
        pass

with open("README.md") as f:
    LONG_DESCRIPTION = f.read()
  
setup(
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    zip_safe=False,
    **meta
)
