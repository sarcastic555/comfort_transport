#!/bin/bash

docker run -it \
    -v ${PWD}/main:/comfort \
    comfort_transport \
    bash
