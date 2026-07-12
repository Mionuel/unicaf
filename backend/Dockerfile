FROM python:3.14-alpine

# create this directory and cd into it
WORKDIR /back-src

# install poetry
RUN pip install poetry==2.4.1

COPY poetry.lock pyproject.toml ./

RUN poetry install

# copy the rest
COPY . .

# venv inside a container lesss go
CMD ["poetry", "run", "fastapi", "run", "src/app.py", "--port", "8000"]
