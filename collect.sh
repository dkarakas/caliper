#!/bin/bash
mkdir -p res
scp $1@$2:/ssd1/$1/gopath/src/github.com/hyperledger/caliper/res/*.out ./res
