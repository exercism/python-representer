#! /bin/sh
DIR="$( dirname "$0" )"
SRC="$( dirname "$DIR" )/src"
export PYTHONPATH="$SRC:$PYTHONPATH"
python bin/generate.py "$@"
