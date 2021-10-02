# BeachScanner

BeachScanner is a python project to download Sentinel-2 data from known beach locations and analyze them for environmental protection.

## Getting started

### Prerequisites

- `python3`

### Creating/updating dependency list

- `pip install pipreqs` (Optional)
- `pipreqs . --force` --> Creates/updates requirements.txt from script imports

Alternatively, you can freeze all installed packages to a requirements file like so:

- `python -m pip freeze`

### Build/Downloading dependencies

- `pip install -r requirements.txt`

or with docker:

- `docker build .` > copies files to docker image and installs requirements.txt

### Running the script

- `python main.py`

or

- `docker run imageName`
