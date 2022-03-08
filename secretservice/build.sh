#!/bin/sh

set -e

mkdir -p out && cd out
cmake -DCMAKE_BUILD_TYPE=Release ../clipboard
cmake --build .
