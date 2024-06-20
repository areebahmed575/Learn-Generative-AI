FROM jupyter/base-notebook:latest

WORKDIR /code

RUN pip install poetry

COPY . . 


RUN poetry install

RUN poetry config virtualenvs.create false

EXPOSE 8000

CMD ["jupyter", "notebook", "--port" , "8888", "--no-browser", "--allow-root"]