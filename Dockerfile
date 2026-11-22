FROM python:3.12-slim

WORKDIR /app

COPY ssh-decoy.py .

ENV PYTHONUNBUFFERED=1

EXPOSE 22/tcp

CMD ["python", "ssh-decoy.py"]
