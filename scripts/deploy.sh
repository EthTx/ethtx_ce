#! /usr/bin/env sh

# Exit in case of error
set -e

dest_dir=../tmp/git_version
chmod +x ./git_version_for_docker.sh
./git_version_for_docker.sh > "$dest_dir"

cd ..

make build-image
make run-database
make run-docker
