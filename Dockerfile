# Change to minimal Python
FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir -r /code/requirements.txt

COPY ./app /code/app

COPY ./weights /code/weights

COPY ./utils /code/utils

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
podman run --rm -e GOOGLE_APPLICATION_CREDENTIALS=/tmp/credentials.json -v $ ml_model_api