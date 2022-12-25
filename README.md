#
<div align="center" height="130px">
  <img src="https://user-images.githubusercontent.com/50231750/209449225-e860408f-5de9-4c8e-ad26-970e514031a6.png" alt="Logotype"/><br/>
  <h1> Done App Backend </h1>
  <p></p>
</div>

> This is the part of the [Done App project](https://github.com/EQSP-Task-Manager)

![CI/CD](https://github.com/EQSP-Task-Manager/backend/actions/workflows/ci-cd-main.yml/badge.svg?branch=main)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![GitHub latest commit](https://badgen.net/github/last-commit/Naereen/Strapdown.js)](https://github.com/EQSP-Task-Manager/backend/commit/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)

## Table of content
- [About](#about)
- [Getting started](#getting-started)
  - [Techical stack](#tech-stack)
- [Run bot](#run)
  - [Without Docker](#without-docker)
  - [With Docker](#with-docker)
- [Deployment](#deploy)
- [License](#license)


## 📎 About application <a name="about"></a>
**Done App** is a mobile application for task management.
 An integral part of this project is application's backend that is presented in this repository.

## 📌 Getting started <a name="getting-started"></a>

### Technical stack <a name="tech-stack"></a>

The backend is written in **Python** programming language and uses PostgreSQL to stora data.
For the sake of convenience of development, several powerful libraries are utilized. 

| Library                                        | Usage                    |
|------------------------------------------------|--------------------------|
| [aiohttp](https://docs.aiohttp.org/en/stable/) | asynchronous HTTP server |
| [sqlalchemy](https://www.sqlalchemy.org/)      | database toolkit         |
 | [pydantic](https://docs.pydantic.dev/)         | data validation          |
| [pytest](https://docs.pytest.org/en/7.2.x/)    | testing tool             |  

## How to run <a name="run"></a>

### Run locally without Docker <a name="without-docker"></a>

#### Requirements

- In order to launch backend locally, firstly one needs to have Python interpreter
  (see [official website](https://www.python.org/downloads/) for the instructions). 
  We used Python **3.10**, therefore we advise to stick with this version. 
  Once interpreter is ready, one needs to install the dependencies.
  ```bash
  pip install -r requirements.txt
  ```

- Another important requirements is to have PostgreSQL server up and running.

#### Start

To start the backend, one needs to set up the arguments.
Currently, there are the following arguments needed:
`API_HOST`, `API_PORT`, `DB_USER` `DB_PASSWORD`, `DB_HOST`, `DB_PORT` and `DB_NAME`.
All of them have default values, so let us further omit some parameters.

To get the description on arguments passing, one can type `python -m backend --help`.

There are several ways how to pass these arguments:

  1) Command line  
     Example:  
     ```bash
     python -m backend --db-user postgres --db-password postgres
     ```

  2) Config file  
     Create `config.yml` file in the project directory and fill it with data (refer to `config-example.yml` for the example).
 
To run, execute the following command: `python -m backend`.
   
### Run using Docker <a name="with-docker"></a>

One needs to install `docker-compose` (see the [instructions](https://docs.docker.com/compose/install/)).
In this case the parameters should be passed via environment variables, see an example:
```bash
DB_USER=postgres DB_PASSWORD=postgres docker-compose up --build
```

## Deployment <a name="deploy"></a>
[Yandex Cloud](https://cloud.yandex.ru/) was used to deploy backend to the server.

## License <a name="license"></a>
Done App Backend is licensed under the MIT License.
This means that you are free to use, modify, and distribute the software as long as you include the appropriate credit and follow the terms of the license.