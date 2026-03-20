FROM python:3.12-slim

WORKDIR /app

COPY app.py .

ENV LOG_INTERVAL=1.0
ENV POD_NAME=local
ENV POD_NAMESPACE=default

CMD ["python", "-u", "app.py"]


