# BeachScanner

This is a python project to download Sentinel-2 data from known beach locations and analyzing them for enviromental protection data.

## Getting started

### Prerequisites

- python3
- venv

## Initializing virtual environment

- `python3 -m venv env`

### Creating/updating dependency list

- `pip install pipreqs` (Optional)
- `pipreqs . --force` --> Creates/updates requirements.txt from script imports

Alternatively you can freeze installed packages to the environment to a requirements file:

- `python3 -m pip freeze`

### Downloading dependencies

- `pip install -r requirements.txt`
