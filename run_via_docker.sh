#!/bin/bash
echo Введите домен

# read domain
$1

# if [ ! dpkg -l | grep docker | awk '{print $2}' &> /dev/null ] 
if [ "$(which docker)" = "" ] 
then
echo "Docker is not installed. Installing Docker..."
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# else
# echo "Docker is already installed."

fi
docker build -t vscaner:1 .
command docker run -it vscaner:1 $1