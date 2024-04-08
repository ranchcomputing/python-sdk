from setuptools import setup
from ranch.__version__ import __version__


requires = ["requests", "bson", "pytest", "twine", "wheel"]

setup(
    name="ranch-sdk",
    version=__version__,
    description="ranchcomputing SDK",
    long_description=open("README.md").read(),
    packages=["ranch"],
    license="MIT",
    install_requires=requires,
    python_requires=">=3.10",
)
