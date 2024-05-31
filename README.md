![PyVulscan](img.webp "PyVulscan")
# <p style="text-align: center;">PyVulscan</p>

## Python vulnerability scanner based on [nmap](http://nmap.org/) and [sqlmap](https://sqlmap.org/)


*Before run scanner on your host make shure that sqlmap and namp installed.*

### TO RUN:
#### Download manyaly or using wget:
```wget https://github.com/Cyb3rFake/PyVulscan.git && cd PyVulscan```

##### Install modules:

```pip install -r requirements```

##### Replace "example.com" with the your scan targer:

```python run.py -d example.com```
***

#### Or use venv
##### Create venv and install modules:
```python -m venv venv && source venv/bin/activate && pip install -r requirements```

##### Replace "example.com" with the your scan targer
```python run.py -d example.com```
***

### TO RUN WITH [DOCKER](https://docs.docker.com/engine/install/ "Docker installation"):
#### install docker manualy [DOCKER](https://docs.docker.com/engine/install/ "Docker installation")
#### or with script:
`sudo sh get-docker.sh` 
#### build docker image:
`DOCKER_BUILDKIT=1 docker build -t scaner:1 .`
##### run dokcer container with argument
`docker run -it --rm scaner:1 examle.com`
***
##### OR run script with argument
`sh run_via_docker.sh example.com`
