FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64
ENV PYSPARK_PYTHON=python

EXPOSE 4040-4050

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        bash \
        openjdk-21-jre-headless \
        procps \
        tini \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app/project

COPY project/ ./

RUN python -m pip install --no-cache-dir --upgrade pip \
    && python -m pip install --no-cache-dir "pyspark>=4.1,<4.2"

ENTRYPOINT ["tini", "--"]
CMD ["python", "easy_run.py", "--help"]
