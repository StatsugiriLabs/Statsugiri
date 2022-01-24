# Environment Setup

## Environment Variables

Run `export $(grep -v '^#' .env | xargs)` in the root directory if you have a `.env` file.

## Python Setup

This guide assumes you have Python 3.9 and `pip` installed. If not, please follow [Python Downloads](https://www.python.org/downloads/) and [PyPi Tutorial](https://pip.pypa.io/en/stable/installation/) to install pip. Check if Python and `pip` are installed by running `Python --version` and `pip --version`.

If you already have a virtual environment set up (or have no need), feel free to run `setup.sh`.

### Virtual Environment

A virtual environment allows developers to isolate their installations.

#### Creating a Virtual Environment

Create a virtual environment at the root of the project directory.

```
python3 -m venv $pwd/..
```

#### Activating the Virtual Environment

Activate the newly created virtual environment.

```
source venv/bin/activate
```

## Go Setup

This guide assumes you have Go 1.17 installed. If not, please follow [Go Downloads](https://go.dev/dl/). Check if Go is installed by running `go version`.
