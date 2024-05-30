FROM ubuntu:jammy

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app
COPY run.py ./
COPY requirements.txt ./

RUN apt-get -y update && apt-get -y upgrade
RUN apt-get install -y git python3-pip nmap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /usr/local/sqlmap &&\
    ln -s /usr/local/sqlmap/sqlmap.py /usr/bin/sqlmap

RUN ln -sf /usr/bin/python3 /usr/bin/python

COPY requirements.txt ./
COPY --chmod=755 run.py ./

RUN pip install -r requirements.txt
# CMD [ "bash" ]
ENTRYPOINT [ "python", "/app/run.py", "-d" ]