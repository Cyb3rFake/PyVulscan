# PyVulscan
## Python vulnerability scanner based on [nmap](http://nmap.org/) and [sqlmap](https://sqlmap.org/)


*Before run scanner on your host make shure that sqlmap and namp installed.*







### TO RUN:
```python run.py -d example.com```

### TO RUN WITH [DOCKER](https://docs.docker.com/engine/install/ "Установка докера"):

#### install docker by script:
`sudo sh get-docker.sh` 
#### build docker image:
`DOCKER_BUILDKIT=1 docker build -t scaner:1 .`
##### run dokcer container with argument
`docker run -it --rm scaner:1 examle.com`
##### OR run script with argument
`sh run_via_docker.sh example.com`
