#!/bin/bash
echo "node ./benchmark/exp/main.js -c $1 1>$2 2>$3"
node ./benchmark/exp/main.js -c $1 1>$2 2>$3
