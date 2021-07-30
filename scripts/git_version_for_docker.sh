#! /usr/bin/env sh

set -e

remote_url_git=$(git config --get remote.origin.url)
remote_url=${remote_url_git::-4}

sha=$(git rev-parse HEAD)
url="${remote_url}/tree/${sha}"

export ETHTX_CE_VERSION=$url
