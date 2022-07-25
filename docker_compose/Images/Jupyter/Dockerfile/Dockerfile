#FROM jupyter/datascience-notebook
FROM  jupyter/tensorflow-notebook
USER root
COPY ./Images/Jupyter/Dockerfile/requirements.txt /home/jovyan/workspace/init_script/requirements.txt

RUN chmod -R 777 /home/jovyan/
RUN apt-get update --yes 
RUN apt-get install --yes --no-install-recommends 
RUN pip install -r /home/jovyan/workspace/init_script/requirements.txt
RUN python -m spacy download pt_core_news_lg