# SentinelScraper

SentinelScraper is a python project to download Sentinel-2 imagery, crop the images, and save them to HDFS.

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

- `python main.py --position 10 11 --fromdate 2021-09-01 --todate 2021-10-12`

or

- `docker run BeachScanner:latest --position 10 11 --fromdate 2021-09-01 --todate 2021-10-12`

## Libraries

- <https://sentinelsat.readthedocs.io/en/stable/index.html>
- geojson.io
