#!/bin/bash
$1


if [ "$(which docker)" = "" ] 
then
echo "Docker is not installed"
echo "Install docker? (y/n)"
read ANSWER

if [ $ANSWER!="y"]
then
echo "install docker manualy and try again..."
exit
fi

curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

fi
DOCKER_BUILDKIT=1 docker build -t vscaner:1 .
command docker run -it vscaner:1 $1