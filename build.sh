#!/bin/bash
export ACCOUNT=123456789012
export REGION=us-east-2
export AWS_PROFILE=default
export REPO_NAME=websocket-test

# invoke this with the version number of the image tag as the first argument
# patch manifest.yaml with the image name/tag.

aws ecr get-login-password --region $REGION | \
           docker login --username AWS --password-stdin $ACCOUNT.dkr.ecr.$REGION.amazonaws.com
aws ecr create-repository --repository-name $REPO_NAME --region $REPO_NAME || true
docker build -t app .
docker tag app  $ACCOUNT.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:v$1
docker push $ACCOUNT.dkr.ecr.$REGION.amazonaws.com/$REPO_NAME:v$1