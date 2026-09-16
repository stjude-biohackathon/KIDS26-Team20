FROM ghcr.io/chroma-core/chroma:1.5.9
# please don't change the above line
# FROM --platform=amd64 ghcr.io/chroma-core/chroma:latest
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV CHROMA_SERVER_NOFILE=${CHROMA_SERVER_NOFILE}
RUN mkdir /code
WORKDIR /code
RUN apt-get update
RUN apt-get install -y --no-install-recommends python3 python3-pip python3-venv build-essential curl
# RUN apt install -y libreoffice
COPY requirements.txt /code/
RUN python3 -m pip install --break-system-packages -r requirements.txt
COPY . /code/