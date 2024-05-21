FROM ubuntu:22.04

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apt-get update
RUN apt install -y python3-pip sqlmap nmap

COPY requirements.txt ./
COPY --chmod=755 run.py ./
RUN pip install -r requirements.txt
ENTRYPOINT [ "/app/run.py", "-d" ]

