#!/bin/bash
DEBUG='debug'
PROD='production'

if [ $# -ne 1 ] || [ $1 != $DEBUG ] && [ $1 != $PROD ]; then
    echo 'usage: ./deploy.sh [debug|production]'
    exit
fi

env=$1

echo -e "[1] start deploy ..."
echo "origin ssh config:"
cat ~/.ssh/config
echo -e "[2] modify ssh config"
if [ $env = $PROD ]; then
    cp ~/.ssh/config_prod ~/.ssh/config
else
    cp ~/.ssh/config_debug ~/.ssh/config
fi

echo -e "new ssh config:"
cat ~/.ssh/config

echo -e "\n[3] start git push ..."
if [ $env = $PROD ]; then
    remote_repo='ssh://ec2-user@remote:/opt/Mongo'
    local_branch='master'
else
    remote_repo='ssh://root@remote:/opt/Mongo'
    local_branch='develop'
fi
echo 'push to '$remote_repo
git push $remote_repo $local_branch
echo "[4] git push completed."

echo -e "\n[5] restore ssh config"
cp ~/.ssh/config_default ~/.ssh/config
echo "origin ssh config:"
cat ~/.ssh/config
echo -e "\n[6] deploy completed."
