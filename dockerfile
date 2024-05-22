FROM alpine:latest

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app

RUN apk update
RUN apk add git python3 py3-pip nmap
RUN git clone --depth 1 https://github.com/sqlmapproject/sqlmap.git /usr/share/sqlmap &&\
    ln -s /usr/share/sqlmap/sqlmap.py /usr/bin/sqlmap

RUN ln -sf /usr/bin/python3 /usr/bin/python

COPY requirements.txt ./
COPY --chmod=755 run.py ./

RUN pip install --break-system-packages -r requirements.txt

ENTRYPOINT [ "python", "/app/run.py", "-d" ]