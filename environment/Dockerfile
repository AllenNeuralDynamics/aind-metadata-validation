# hash:sha256:9455a1c99c2ed00d789b81cfb8c319a36be678a6e0dbc6f75c39a2ddd22165ef
FROM registry.codeocean.allenneuraldynamics.org/codeocean/jupyterlab:3.0.9-miniconda4.9.2-python3.8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN conda install -y \
        pandas==1.5.3 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    aind-codeocean-api==0.2.3 \
    aind-data-access-api==0.3.1 \
    boto3==1.28.11 \
    pymongo==4.4.1
