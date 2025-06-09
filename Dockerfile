FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    default-mysql-client \
    gcc \
    pkg-config \
    libmariadb-dev \
    curl \
    && apt-get clean

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . . 

ADD https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 /cloud_sql_proxy
RUN chmod +x /cloud_sql_proxy

ENV GOOGLE_APPLICATION_CREDENTIALS="/key.json"

EXPOSE 8080

CMD ["sh", "-c", "./cloud_sql_proxy -dir=/cloudsql -instances=turnkey-chimera-460001-p0:us-central1:freshguard-uas & python app.py"]
