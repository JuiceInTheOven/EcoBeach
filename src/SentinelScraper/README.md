# SentinelScraper

SentinelScraper is a Kafka producer to download Sentinel-2 imagery, crop the images, mask it with a black and white filter, and save them to a Kafka topic.

## Getting started

### Prerequisites

- `python3`

### Build/Downloading dependencies

- `pip install -r requirements.txt`

or with docker:

- `docker build -t BeachScanner:latest .` > copies files to docker image, installs requirements.txt and sets executable for the image.

### Running the script

- `python main.py`

or

- `docker run BeachScanner:latest`

The script supports the following 3 optional arguments:

- `--days 365` scrapes for imagery for the last year. Defaults to 7 days.
- `--username someUser` username for Cupernicus. Defaults to Nikolai's username.
- `--password ****` passford for Cupernicus. Defaults to Nikolai's password.

## Libraries

- [Sentinel2Loader](https://github.com/flaviostutz/sentinelloader)
