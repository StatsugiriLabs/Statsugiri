#!/bin/bash

#
# This script is used to authenticate the Docker CLI to the ECR registry
# https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html
# 

if [ "$#" -ne 1 ]; then
    echo "Please provide 1 argument, 'ACCOUNT_ID'"
    exit 1
fi

ACCOUNT_ID=$1
REGION="us-west-2"

aws ecr get-login-password --region $REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com
