# Installation

We recommend you to set up a Python virtual environment.
To do so with Python2 you need `virtualenv`, you should be able to install it using for
example one of the following commands:

```bash
apt-get install python-virtualenv
easy_install virtualenv
pip install virtualenv
```

Or for Python3:

```bash
apt-get install python3-venv
pip3 install virtualenv
```

Once `virtualenv` is installed you can create your own environment by running
the following commands in the project directory:

```bash
python3 -m venv venv
```

Then each time you want to use your virtual environment you have to activate it
by running this command:

```bash
. venv/bin/activate
```
Finally you have to install in your environment the ranch SDK:

```bash
pip install ranchcomputing
```

If you plan to send large files to the API, we advise you to install the
optional requests-toolbelt dependency in order not to overuse your memory:

You are now ready to use the ranch SDK.