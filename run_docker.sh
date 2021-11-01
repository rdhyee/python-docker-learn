#!/bin/bash

set -e
docker build -t rdhyee/python-docker-learn .
docker run -it --rm \
   -v "$PWD":/usr/src/app \
   --name python-docker-learn \
   rdhyee/python-docker-learn \
   python script.py
