# BeachScanner

BeachScanner is a python project to download Sentinel-2 data from known beach locations and analyze them for environmental protection.

## Getting started

### Prerequisites

- `python3`
- `venv`

## Working with virtual environment

- Initialize: `python3 -m venv venv`
- Activate: `source ./venv/bin/activate`
- Deactivate: `deactivate`

### Creating/updating dependency list

- `pip install pipreqs` (Optional)
- `pipreqs . --force` --> Creates/updates requirements.txt from script imports

Alternatively, you can freeze all installed packages to a requirements file like so:

- `python3 -m pip freeze`

### Downloading dependencies

- `pip install -r requirements.txt`
