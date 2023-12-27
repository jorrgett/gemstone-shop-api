FROM python:3.11

# Preparing the application to run inside the container
WORKDIR /code

COPY ./ /code

RUN pip install -r requirements.txt

CMD uvicorn app.main:app --reload --host 0.0.0.0 --port 8000