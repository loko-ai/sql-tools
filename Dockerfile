FROM python:3.10-slim
EXPOSE 8080
RUN apt-get update --fix-missing && apt-get install -y wget curl build-essential
RUN wget https://r.mariadb.com/downloads/mariadb_repo_setup && chmod +x mariadb_repo_setup && ./mariadb_repo_setup
RUN apt install -y libmariadb3 libmariadb-dev
RUN pip install --upgrade pip
CMD echo "hello"
ADD ./requirements.lock /
RUN pip install -r /requirements.lock
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR /plugin/services
CMD python services.py