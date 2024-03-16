FROM python:3.11.8-slim-bookworm
COPY /app /app
COPY /requirements.txt /requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends libpq-dev gcc python3-dev
RUN pip install --no-cache-dir --upgrade pip -r /requirements.txt

WORKDIR /app

ENTRYPOINT ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
