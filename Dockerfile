FROM python:3.6.2
RUN apt-get install -y curl \
    && curl -sL https://deb.nodesource.com/setup_13.x | bash - \
    && apt-get install -y nodejs \
    && curl -L https://www.npmjs.com/install.sh | sh
ENV PYTHONUNBUFFERED 1
RUN mkdir /work
WORKDIR /work
COPY . /work
RUN pip install -r requirements/base.txt
RUN pip install -r requirements/production.txt
