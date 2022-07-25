FROM puckel/docker-airflow:1.10.9 
####docker.io/bitnami/airflow:2
USER root
COPY ./Images/Airflow/Dockerfile/requirements.txt /home/requirement_scripts/requirements.txt

RUN apt-get update --yes 
RUN apt-get install --yes --no-install-recommends 
RUN pip install -r /home/requirement_scripts/requirements.txt