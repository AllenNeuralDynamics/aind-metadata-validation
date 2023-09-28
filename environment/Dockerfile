# hash:sha256:a07d283ddd89d48b38b8d3d35c28dd4d18099f8d4ffc8399e8561e2d9a505c04
FROM registry.codeocean.allenneuraldynamics.org/codeocean/jupyterlab:3.0.9-miniconda4.9.2-python3.8-ubuntu20.04

ARG DEBIAN_FRONTEND=noninteractive

ARG GIT_ASKPASS
ARG GIT_ACCESS_TOKEN
COPY git-askpass /

RUN conda install -y \
        pandas==1.5.3 \
        seaborn==0.12.2 \
    && conda clean -ya

RUN pip install -U --no-cache-dir \
    aind-codeocean-api==0.2.3 \
    aind-data-access-api==0.3.1 \
    boto3==1.28.11 \
    pymongo==4.4.1
