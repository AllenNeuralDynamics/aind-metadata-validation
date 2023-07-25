# hash:sha256:2e8090579994505da3e0613f6483849dabb87ca268a5a02772b0563a4f1d0bd0
FROM registry.codeocean.allenneuraldynamics.org/codeocean/jupyterlab:3.0.9-miniconda4.9.2-python3.8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN pip install -U --no-cache-dir \
    aind-codeocean-api==0.2.3 \
    aind-data-access-api==0.3.1 \
    pymongo
