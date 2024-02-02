# Flex Power Engineering Challenge [WIP]

> This repository tries to implement the code challenge proposed by <https://github.com/FlexPwr/EngineeringChallenge>

## Overview

## Dependencies

* `docker` and `docker-compose`
* `poetry`

## How to run

```sh
 cp .env.example .env # Change values
 poetry shell
 task run
```

## Commands

* `task run` - start docker container define on `docker-compose.yml`
* `task clean`- stop and clean containers created by the command `task run`
* `task lint` - run lint
* `test test`- run tests
