FROM python:3.12.0-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV WAIT_VERSION 2.7.2
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/$WAIT_VERSION/wait /wait
RUN chmod +x /wait

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]