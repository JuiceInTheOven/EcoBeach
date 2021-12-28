# ms-semesterproject

## Getting started

### Prerequisites

Required software:

- Docker
- LaTeX
  - LaTeX Workshop (if using VSCode)
- .NET-6.0rc1 (because Nikolai runs on the Apple M1 processor, this or a newer version is required)

## LaTeX Report

The report lives under /report. The LaTeX project is setup to follow the style of scientific reports. Frontmatter contains all content before the first chapter. Such as the Abstract, Title page etc. The Mainmatter contains all the chapters of the report, and lastly the backmatter contains all the content after the last chapter.

If you need help with LaTeX let me (Nikolai) or Niels know.

## Services/Applications

### SentinelSatDownloader

A service capable of downloading images from the Sentinel Sattelite given a position and a timeframe.

### WebApi

The WebApi project is a simple .NET-6.0 backend project with an API to communicate to our Kafka and Hadoop processing pipeline. Swagger is enabled by default.

### Local run

1. Run docker-compose files in .docker

Kowl (localhost:8088)

Spark (localhost:8080)

### Docker Swarm

- Hadoop
- Kafka

Kafka Servers:

- helsinki.faurskov.dev:9092 (Most likely the master)
- nuremberg.faurskov.dev:9092
- falkenstein.faurskov.dev:9092

Dev services:

- <http://135.181.80.186:8080/brokers> (Kowl webui)