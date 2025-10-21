
FROM python:3.11

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

COPY ./data /code/data

COPY ./.env /code/.env

COPY ./templates /code/templates


EXPOSE 8032

CMD ["fastapi", "run", "app/main.py", "--port", "8032"]