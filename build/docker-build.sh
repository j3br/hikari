#!/bin/bash

VERSION=$(cat ../hikari/__init__.py | grep '__version__' | cut -d'"' -f2)
REPO="j3br/hikari"

# Build image with module version number and 'latest' tags
docker build -t "$REPO":$VERSION -t "$REPO":latest ../