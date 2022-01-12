#!/bin/bash

#
# This script is used for tagging and pushing the DataExtractor image for AWS Lambda
# Assume `create-repository` has been run for Amazon ECR and Docker CLI has been authenticated
# See: https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
#

if [ "$#" -ne 2 ]; then
    echo "Please provide 2 arguments, IMAGE and ACCOUNT_ID"
    exit 1
fi

CURR_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR="$CURR_DIR/../src"
REGION="us-west-2"
IMAGE=$1
ACCOUNT_ID=$2

cd $SRC_DIR/data_pipeline

# Build image
docker build -t $IMAGE .
# Tag and upload 
docker tag $IMAGE:latest $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$IMAGE:latest
docker push $ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$IMAGE:latest
