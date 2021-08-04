#! /usr/bin/env bash

# Execute in root project directory
# Exit in case of error
set -e

remote_url=$(git config --get remote.origin.url)
sha=$(git rev-parse HEAD)

# url, sha
url_sha="${remote_url},${sha}"

# return
echo "$url_sha"
