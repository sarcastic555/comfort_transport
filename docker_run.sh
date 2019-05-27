#!/bin/bash

docker run -it --rm \
    -p 8080:8080 \
    -v ${PWD}/main:/comfort_transport \
    comfort_transport \
    bash
