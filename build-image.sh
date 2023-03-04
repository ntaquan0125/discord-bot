#!/usr/bin/env bash

echo "Input number to choice release version or test version"
echo "1: release"
echo "2: test"

read release

echo "Input number to choice image architectures"
echo "1: arm64/aarch64"
echo "2: x86_64/amd64"

read architectures

echo "Input password"
read pwds

echo "Prepare for building image"

if [[ "$release" == "1" ]]; then
    name="botpif"
    target="--target prod"
elif [[ "$release" == "2" ]]; then
    name="botpif_test"
    target="--target dev"
fi

name_file="${name}.tar"
docker_path="docker/Dockerfile"

echo ${pwds} | sudo -S rm ${name_file} 2>/dev/null|| echo

echo "Building image"

if [[ "$architectures" == "1" ]]; then
    echo "Arm64/aarch64 selected"
    docker buildx build --platform=linux/arm64/v8 -f ./docker/Dockerfile -t ${name} ${target} .
elif [[ "$architectures" == "2" ]]; then
    echo "x86_64/amd64 selected"
    docker buildx build --platform=linux/amd64 -f ./docker/Dockerfile -t ${name} ${target} .
fi
