# ux-analytics-data-pipeline

This is a simple data pipeline for the UX Analytics team.

## Arhitecture Diagram

![Arhitecture Diagram](https://github.com/vignesh-codes/ux-analytics-data-pipeline/blob/main/arch_diagram.png)

## How to use this repository
1. Clone the repository to your local machine.
2. This repository demonstrates a data pipeline for UX Analytics. It includes data ingestion, data processing, and data visualization. The data pipeline is built using Kafka, Zookeper, Postgres, and Docker.
3. Use the AI Agent MCP Server to analyse the data and generate insights and reports using this repo https://github.com/vignesh-codes/ai-agents-mcp-pg.
4. Pull the Metabase Docker Image
```
docker pull metabase/metabase:latest
```
5. Run the Metabase Docker
```
docker run -d -p 3000:3000 --name metabase metabase/metabase
```

## Requirements
- docker
- docker-compose
- python 3.8
- claude desktop

## Usage
To run the pipeline, execute the following command in your terminal:

```bash
docker-compose -d up
```

This will start the kafka, zookeper, postgres containers in detached mode.

To run the api server, execute the following command in your terminal:

```bash
python api-server.py
```
This will start the api server.

To run the kafka consumer, execute the following command in your terminal:

```bash
python kafka-consumer.py
```
This will start the kafka consumer.

To run the client, execute the following command in your terminal:

```bash
python client.py
```
This will start the client throwing lots of dummy data into the api-server that goes to kafka topic.
