#!/bin/bash
$1

if [ "$EUID" -ne 0]
    then echo "Please run as root"
    exit
fi


if [ "$(which docker)" = "" ] 
    then
        echo "Docker is not installed"
        echo "Install docker? (y/n)"
        read ANSWER

        if [ "$ANSWER" -ne "y" ]
            then
                echo "install docker manualy and try again..."
                exit
        fi

    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh

fi

DOCKER_BUILDKIT=1 docker build -t vscaner:1 .
command docker run -it --rm --name scaner vscaner:1 $1
