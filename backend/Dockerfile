FROM python:3.14-alpine

# create this directory and cd into it
WORKDIR /backend

# install poetry
RUN pip install poetry==2.4.1

COPY poetry.lock pyproject.toml ./

RUN poetry install

# copy the rest
COPY . .

# venv inside a container lesss go
CMD ["poetry", "run", "fastapi", "dev", "src/app.py", "--host", "0.0.0.0", "--port", "8000"]
