FROM ubuntu:22.
RUN mkdir areeb
RUN apt update

FROM python:3.12
RUN pip install poetry
WORKDIR /code
ADD ./pyproject.toml  /code/
ADD ./docker_debug /code/docker_debug/
RUN poetry install
CMD [ "poetry", "run", "uvicorn", "docker_debug.main:app", "--host", "0.0.0.0"]