#!/bin/bash

docker buildx build --platform linux/arm/v7 --tag $IMAGE --push $BUILD_CONTEXT
