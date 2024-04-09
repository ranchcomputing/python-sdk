from setuptools import setup
from ranch.__version__ import __version__


requires = ["requests", "bson", "twine", "wheel", "boto3", "tuspy"]

setup(
    name="ranch-sdk",
    version=__version__,
    description="ranchcomputing SDK stands as a bridge between external pipelines and our rendering services",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://www.ranchcomputing.com",
    author="mohamed bakhouche",
    author_email="dev@ranchcomputing.com",
    license="MIT",
    project_urls={
        "Documentation": "https://download.ranchcomputing.com/dl/ranch_online/ranchsdk/guide/usage.html",
        "Source": "https://github.com/ranchcomputing/python-sdk"
        },
    packages=["ranch"],
    python_requires=">=3.10,<3.14",
    install_requires=requires,
    include_package_data=True, 
    classifiers=["Development Status :: 3 - Alpha",
                   "Intended Audience :: Developers",
                   "Topic :: Utilities",
                   "Programming Language :: Python :: 3.10",
                   "Programming Language :: Python :: 3.11",
                   "Programming Language :: Python :: 3.12",
                   "Programming Language :: Python :: 3.13",
                   "License :: OSI Approved :: Apache Software License"],
)
