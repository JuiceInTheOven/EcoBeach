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

- `docker build -t BeachScanner:latest .` > copies files to docker image, installs requirements.txt and sets executable for the image.

### Running the script

- `python main.py --position 10 11 --fromdate 20200901 --todate NOW`

or

- `docker run BeachScanner:latest --position 10 11 --fromdate 20200901 --todate NOW`

## Libraries

- <https://sentinelsat.readthedocs.io/en/stable/index.html>
- geojson.io
