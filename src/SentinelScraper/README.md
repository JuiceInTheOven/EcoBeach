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

## Libraries

- [Sentinel2Loader](https://github.com/flaviostutz/sentinelloader)
