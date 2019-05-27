#!/bin/bash

docker run -it \
    -v ${PWD}/main:/comfort_transport \
    comfort_transport \
    bash
