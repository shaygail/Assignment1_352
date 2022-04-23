FROM python:3.10

COPY . .

WORKDIR /

ENV PYTHONUNBUFFERED=1

CMD ["python", "server3.py"]