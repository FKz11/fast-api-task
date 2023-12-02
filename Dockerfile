FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt /app
COPY main.py /app

RUN pip install -r requirements.txt

CMD ["python", "main.py"]
