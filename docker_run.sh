#!/bin/bash

docker run -it --rm \
    -p 5000:5000 \
    -v ${PWD}/main:/comfort_transport \
    comfort_transport \
    bash
