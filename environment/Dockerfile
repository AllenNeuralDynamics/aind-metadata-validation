# hash:sha256:ffdd39cd1170a4286607cff69f102c1dd4eaa5ee3d645ea077ce0f2e779530d7
FROM registry.codeocean.allenneuraldynamics.org/codeocean/jupyterlab:3.0.9-miniconda4.9.2-python3.8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY
ARG CUSTOM_KEY
ARG CUSTOM_KEY_2
ARG CUSTOM_KEY_3

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN conda install -y \
        pandas==1.5.3 \
        seaborn==0.12.2 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    aind-codeocean-api==0.4.1 \
    aind-data-access-api==0.6.2 \
    aind-data-schema==0.26.6 \
    boto3==1.28.11 \
    pymongo==4.4.1
