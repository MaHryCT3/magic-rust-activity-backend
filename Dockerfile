FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install --no-install-recommends -y \
    git \
    binutils \
    libpq-dev \
    ffmpeg \
    gcc  && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code
COPY . /code

EXPOSE 8000
