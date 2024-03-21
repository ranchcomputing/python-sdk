Boto3 Documentation

Documentation for ranch sdk can be found `here <https://ranchcomputing.com>`_.

Generating Documentation

Note: Botocore's `requirement-docs.txt <https://github.com/boto/botocore/blob/develop/requirements-docs.txt>`_ must be installed prior to attempting the following steps.

Sphinx is used for documentation. You can generate HTML locally with the
following:

Install sphinx

https://sphinx-themes.org/


$ mkdir docs
$ cd docs

$ pip install sphinx
$ pip install furo
$ pip install myst-parser

$ sphinx-quickstart

$ cd ..
$ sphinx-apidoc -o docs src

$ pip install -r requirements-docs.txt
$ mkdir docs
$ cd docs
$ make html