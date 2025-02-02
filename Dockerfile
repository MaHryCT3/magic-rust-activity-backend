FROM python:3.12-slim
ENV PYTHONUNBUFFERED 1

RUN apt-get update &&  \
    apt-get install --no-install-recommends -y \
    git \
    binutils \
    libpq-dev\
    gcc  && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /code
COPY . /code

RUN chmod +x /code/.dockerinit.sh

CMD [ "/code/.dockerinit.sh" ]
EXPOSE 8000
