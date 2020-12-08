#!/bin/bash

if [ $# -ne 1 ]; then
    echo $0: usage: sh start.sh sessionname
    exit 1
fi

SESSION_NAME=$1

anyscale up $SESSION_NAME \
    --config cluster.yaml \
    --cloud-name anyscale_default_cloud