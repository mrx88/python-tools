FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt ./

COPY main.py ./
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["/app/main.py"]