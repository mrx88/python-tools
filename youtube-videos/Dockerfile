FROM python:3.10-slim-bullseye

WORKDIR /app

COPY requirements.txt ./

COPY main.py ./
RUN pip install --no-cache-dir -r requirements.txt


ENTRYPOINT ["/app/main.py"]