#!/bin/bash

set -e
docker build -t rdhyee/python-docker-learn .
docker run -it --rm -v "$PWD":/usr/src/myapp -w /usr/src/myapp --name python-docker-learn rdhyee/python-docker-learn
