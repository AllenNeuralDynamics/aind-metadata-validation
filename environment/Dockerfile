# hash:sha256:afa30fcafbb000de1a970838f01e6d9ae44c6de4524a36d8cdfd4d1e5fa2fbb8
ARG REGISTRY_HOST
FROM $REGISTRY_HOST/codeocean/jupyterlab:3.0.9-miniconda4.9.2-python3.8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG AWS_ACCESS_KEY_ID
ARG AWS_DEFAULT_REGION
ARG AWS_SECRET_ACCESS_KEY
ARG CUSTOM_KEY
ARG CUSTOM_KEY_2
ARG CUSTOM_KEY_3
ARG CUSTOM_KEY_4
ARG CUSTOM_KEY_5
ARG CUSTOM_KEY_6
ARG CUSTOM_KEY_7
ARG CUSTOM_KEY_8

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN conda install -y \
        pandas==1.5.3 \
        seaborn==0.12.2 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    aind-codeocean-api==0.4.1 \
    aind-data-access-api[docdb]==0.11.0 \
    aind-data-schema==0.38.5 \
    boto3==1.28.11 \
    pymongo==4.4.1 \
    pyopenssl==24.1.0

ADD "https://github.com/coder/code-server/releases/download/v4.9.0/code-server-4.9.0-linux-amd64.tar.gz" /.code-server/code-server.tar.gz
	
RUN cd /.code-server \
	&& tar -xvf code-server.tar.gz \
	&& rm code-server.tar.gz \
	&& ln -s /.code-server/code-server-4.9.0-linux-amd64/bin/code-server  /usr/bin/code-server
