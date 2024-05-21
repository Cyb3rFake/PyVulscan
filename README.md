# PyVulscan
Python vulnerability scanner based on nmap and sqlmap
TO RUN:
python run.py -d example.com

TO RUN WITH DOCKER:

install docker by script ```sudo sh get-docker.sh```
```DOCKER_BUILDKIT=1 docker build -t scaner:1 .```
```docker run -it --rm scaner:1 examle.com```

OR
```sh run_via_docker.sh example.com```