# simple_todo_api

## Local

###  Installation

Make sure you have [poetry](https://python-poetry.org/docs/#installation) installed.


```bash
# clone this repo
git clone https://github.com/lbellomo/simple_todo_api.git
cd simple_todo_api
# install dependencies 
poetry install
# activate the virtual env
poetry shell
```

### Run

To run it make sure you have the virtual env activated (with `poetry shell`)

```bash
uvicorn app.main:app
# or run with hot-reload
# uvicorn app.main:app --reload
```

You can look at the api documentation at `http://127.0.0.1:8000/docs` or `http://127.0.0.1:8000/redoc`

To run the tests simply do:

```bash
pytest
```

## Docker

### Setup

```bash
# clone this repo
git clone https://github.com/lbellomo/simple_todo_api.git
cd simple_todo_api

docker-compose build
```

### Run

```bash
docker-compose up
# in the browser go to http://localhost:8000/docs
```

