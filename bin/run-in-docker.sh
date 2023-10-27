#!/usr/bin/env bash
set -e

# Synopsis:
# Analysis runner for run.sh in a docker container
# Takes the same arguments as run.sh (EXCEPT THAT SOLUTION AND OUTPUT PATH ARE RELATIVE)
# Builds the Dockerfile
# Runs the docker image passing along the initial arguments

# Arguments:
# $1: exercise slug
# $2: **RELATIVE** path to solution folder (with trailing slash)
# $3: **RELATIVE** path to output directory (with trailing slash)

# Output:
# Writes the analyasis results to a analyasis.json file in the passed-in output directory.
# The results are formatted according to the specifications at https://github.com/exercism/docs/blob/main/building/tooling/analyzers/interface.md

# Example:
# ./run-in-docker.sh two-fer ./relative/path/to/two-fer/solution/folder/ ./relative/path/to/output/directory/

# If arguments not provided, print usage and exit
if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
    echo "usage: run-in-docker.sh exercise-slug ./relative/path/to/solution/folder/ ./relative/path/to/output/directory/"
    exit 1
fi

# build docker image
docker build --rm -t exercism/python-representer .

# Create output directory if it doesn't exist
output_dir="$3"
mkdir -p "$output_dir"

# run image passing the arguments
docker run \
    --rm \
    --network none \
    --read-only \
    --mount type=bind,src=$PWD/$2,dst=/solution \
    --mount type=bind,src=$PWD/$output_dir,dst=/output \
    --mount type=tmpfs,destination=/tmp \
    exercism/python-representer $1 /solution/ /output/
