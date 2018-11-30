FROM python:3.6

RUN mkdir -p /usr/src/app &&\
    apt update &&\
    apt install -y libyajl-dev

WORKDIR /usr/src/app
COPY . /usr/src/app

RUN pip install pipenv
RUN pipenv install --system --deploy

ENTRYPOINT ["py.test"]
