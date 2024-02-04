# Flex Power Engineering Challenge

> This repository tries to implement the code challenge proposed by <https://github.com/FlexPwr/EngineeringChallenge>

## Overview

### Task 1 - API

The API is implemented using the frameworks [FastAPI](https://fastapi.tiangolo.com/) and [SQLModel](https://sqlmodel.tiangolo.com/), the API project is inspired by <https://github.com/rodrigodelmonte/text-summarizer/>,
however, using more recent tools like [SQLModel](https://sqlmodel.tiangolo.com/) that combine Pydantic and SQLAlchemy models.

### Task 2 - Workflow Ingest EPEX Trades

The Workflow is implemented using Airflow DAGs, taking advantage of the built-in Hooks and Operators. The workflow `dags/trade_report_dag.py` reads
CSVs files from `data/` and ingests into the API developed in task 1.

### Task 3 - Workflow Generate Profit and Loss Report

The workflow `dags/pnl_report_dag.py` is generated using the API database as the data source and target for the `PNL` report. the report results can be viewed
using the `cli/pnl_report.py`, check the Python script to know the required environment variables.

## Dependencies

* `docker` and `docker-compose`
* `poetry`

## How to run

```sh
cp .env.example .env # Change values
cp .env.airflow.example .env.airflow # Change values
poetry shell
poetry install
poetry run task test # Running tests
poetry run task airflow_init # Setup Airflow
poetry run task run # Init Airflow and Backend API
# Airflow should be exposed in the address http://0.0.0.0:8080 user: airflow, pass: airflow
# The API should be exposed in the address http://0.0.0.0:8000 user and pass defined in the .env file
poetry run task clean # stop and and rm the containers
```

## Commands

* `task run` - start docker container define on `docker-compose.yml`
* `task clean`- stop and clean containers created by the command `task run`
* `task lint` - run lint
* `task test`- run tests
* `task airflow_init` - Init Airflow

## Project Structure

```
├── cli                 # Python CLI script to print PNL Reports in the Terminal. Task 3.
├── dags                # Airflow DAGs to Task 2 and Task 3 of the code challenge
├── data                # Generated sample data to test API and Workflows
├── docker-compose.yml  # Airflow docker-compose + API services definitions
├── flexpower           # API project
├── include             # SQL query to generate PNL report
├── README.md           # This file!
└── tests               # API tests
```

## Considerations

*The following considerations are key areas I consider need to be addressed before a production release. Please note that this list may not cover all important aspects, but it highlights a starting point of priorities:

* It would be good to have a staging environment. it is not trivial for the data pipelines, but it helps tests huge structural changes.
* The project does not have CI/CD pipeline, Github Actions could be used to automate some steps to release the backend API.
* The solution does not have monitoring or observability mechanisms, [OpenTelemetry](https://opentelemetry.io/docs/) could be considered here to address this capability.
* The solution also does not have alerts and notification mechanisms in case of failures.
* Test the solution with the expected number of records and files estimated for production.
* Review test scenarios.
* Test the solution to recover from failures, test data consistency after reprocess reports and backfill Airflow DAGs.
* Add data validation tests.
* Explore the usage of the tool [Timescale](https://docs.timescale.com/) to expose metrics to users via a Grafana dashboard.
