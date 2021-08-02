#!/bin/bash

# Exit in case of error
# make sure that you are in `scripts` dir
set -e

dest_dir=../tmp/git_version
chmod +x ./git_version_for_docker.sh
./git_version_for_docker.sh > "$dest_dir"

cd ..

make build-image
make run-database
make run-docker
